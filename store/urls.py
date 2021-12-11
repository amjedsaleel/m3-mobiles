# Django
from django.urls import path

# local Django
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('product-details/<str:brand_slug>/<str:variant_slug>/', views.product_details, name='products-details'),
    path('filter/<str:brand_slug>/', views.brand_wise, name='brand-wise'),
    path('search/', views.search, name='search')
]
