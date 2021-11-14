# Django
from django.urls import path

# local Django
from . import views

app_name = 'admin-panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout', views.logout, name='logout'),

    path('brands/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add-brand'),
    path('filter/<str:id>/', views.brand_wise_variant, name='brand-wise-variant'),
    path('edit-brand/<str:brand_id>/', views.edit_brand, name='edit-brand'),
    path('delete-brand/<str:brand_id>/', views.delete_brand, name='delete-brand'),

    path('products/', views.all_products, name='products'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit-product/<str:product_id>/', views.edit_product, name='edit-product'),
    path('delete-product/<str:product_id>/', views.delete_product, name='delete-product'),

    path('add-variant/', views.add_variant, name='add-variant'),
    path('edit-variant/<str:product_id>/', views.edit_variant, name='edit-variant'),
    path('delete-variant/<str:id>/', views.delete_variant, name='delete-variant'),
]
