# Django
from django.urls import path

# local Django
from . import views

app_name = 'admin-panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('brands/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add-brand'),
    path('products/', views.product, name='products'),
    path('add-product/', views.product_add, name='add-product')
]
