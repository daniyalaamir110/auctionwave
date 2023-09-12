from django.contrib import admin
from .models import Category, Product, Bid

# Register your models here.
admin.register(Category, Product, Bid)
