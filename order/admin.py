# Django
from django.contrib import admin

# local Django
from .models import Order, OrderProduct

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
