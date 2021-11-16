# Django
from django.contrib import admin

# local Django
from .models import Cart, CartItem

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
