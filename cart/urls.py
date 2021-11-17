# Django
from django.urls import path

# local Django
from .import views

app_name = 'cart'

urlpatterns = [
    path('', views.user_cart, name='cart'),
    path('add-to-cart/<str:variant_slug>/', views.add_to_cart, name='add-to-cart'),
    path('increment-cart-item/<str:cart_item_id>/', views.increment_cart_item, name='increment-cart-item'),
    path('decrement-cart-item/<str:cart_item_id>/', views.decrement_cart_item, name='decrement-cart-item')

]
