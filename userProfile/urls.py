# Django
from django.urls import path

# local Django
from . import views

app_name = 'userProfile'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my-addresses/', views.my_addresses, name='my-addresses'),
    path('edit-address/<str:pk>/', views.edit_address, name='edit-address'),
    path('delete-address/<str:pk>/', views.delete_address, name='delete-address'),
    path('set-default-address/<str:pk>/', views.set_default_address, name='set-default-address')
]