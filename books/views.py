from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Book, Rating, Category
from accounts.models import Borrow, Profile
from .forms import RatingForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



# Create your views here.

def send_email(user, context):
    template = 'sendmail.html'
    to = user.email
    subject = context['subject']
    message = render_to_string(template, context)
    send_email = EmailMultiAlternatives(subject, '', to=[to])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

class BookView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class BookDetailView(DetailView, FormView):
    model = Book
    template_name = 'book.html'
    form_class = RatingForm
    context_object_name = 'book'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('book', kwargs={'pk': self.object.pk})
        else:
            return reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = Rating.objects.filter(book=self.get_object())
        context['form'] = self.get_form()
        return context
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.book = self.get_object()
            form.instance.User = self.request.user
            form.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
class BorrowBookView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    def get(self, request, id):
        profile = get_object_or_404(Profile, user=request.user)
        books = Book.objects.filter(pk=id)
        if profile.balance >= books[0].price:
            profile.balance-=books[0].price
            borrow = Borrow.objects.create(user=request.user)
            borrow.book.set(books)
            profile.save()
            messages.success(request, 'Your Borrow is Successful')
            send_email(self.request.user, {'subject': 'Borrow Book Confirm', 'user': self.request.user, 'borrow': borrow, 'book': books[0]})
            return redirect('borrows')
        else:
            messages.warning(request, 'Your Balance is Low, Add Balance')
            return redirect('add_money')
        
    
class ReturnBorrowView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, id):
        borrow = get_object_or_404(Borrow, id=id)
        profile = get_object_or_404(Profile, user=request.user)
        profile.balance+=borrow.book.first().price
        profile.save()
        borrow.return_book = True
        borrow.save()

        return redirect('borrows')

def books(request):
    return render(request, 'books.html')
