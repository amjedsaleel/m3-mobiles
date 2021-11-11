# Django
from django.contrib import admin

# local Django
from .models import Product

# Register your models here.

admin.site.register(Product)
