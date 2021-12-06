# Django
from django.contrib import admin

# local Django
from .models import Product, Variant, ReviewRating

# Register your models here.

admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(ReviewRating)
