from django.contrib import admin
from .models import Book, Rating, Category
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category']
    list_filter = ['title', 'price']
    search_fields = ['title']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['book', 'rating', 'date']


admin.site.register(Book, BookAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Category)
