# Django
from django.urls import path

# local Django
from .import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<str:variant_slug>/', views.add_to_cart, name='add-to-cart')
]
