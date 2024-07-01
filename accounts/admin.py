from django.contrib import admin
from .models import Transation, Profile, Borrow
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'date']

admin.site.register(Transation, TransactionAdmin)
admin.site.register(Profile)
admin.site.register(Borrow)
