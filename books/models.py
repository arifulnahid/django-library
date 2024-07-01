from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from .constant import RATTING

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    price = models.IntegerField()
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Rating(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATTING, default=1)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.book.title
