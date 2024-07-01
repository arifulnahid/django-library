from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username


class Borrow(models.Model):
    book = models.ManyToManyField(Book)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    return_book = models.BooleanField(default=False)


class Transation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.user} {self.amount}'
