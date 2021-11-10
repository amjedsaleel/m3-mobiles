# Django
from django.contrib import admin

# local Django
from .models import CustomUser

# Register your models here.

admin.site.register(CustomUser)
