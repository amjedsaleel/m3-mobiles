# Django
from django.urls import path

# local Django
from .import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart')
]
