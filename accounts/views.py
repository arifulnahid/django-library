from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMultiAlternatives
from django.views.generic import DetailView, ListView
from django.contrib.auth import logout, login
from django.template.loader import render_to_string
from .forms import UserSignupForm, UserLoginForm, AddMoneyForm
from .models import Profile, Borrow

# Create your views here.

def send_email(user, context):
    template = 'diposit_email.html'
    to = user.email
    subject = context['subject']
    message = render_to_string(template, context)
    send_email = EmailMultiAlternatives(subject, '', to=[to])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()



class UserSignupView(FormView):
    template_name = 'signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')


def user_logout(request):
    logout(request)
    return redirect('login')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    model = Profile
    template_name = "profile.html"
    context_object_name = 'profile'



class AddMoneyView(LoginRequiredMixin,FormView):
    login_url = '/accounts/login/'
    template_name = 'add_money.html'
    form_class = AddMoneyForm

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user_id})

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user = self.request.user
        form.instance.user = user
        profile = Profile.objects.get(user=self.request.user)
        profile.balance+=amount
        profile.save()
        form.save()
        send_email(user, {"amount": amount, 'subject': 'Diposit Money'})
        return super().form_valid(form)
    

class BorrowListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    model = Borrow
    template_name = 'borrow.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset