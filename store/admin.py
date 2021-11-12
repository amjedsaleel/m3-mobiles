# Django
from django.contrib import admin

# local Django
from .models import Product, Variant

# Register your models here.

admin.site.register(Product)
admin.site.register(Variant)

