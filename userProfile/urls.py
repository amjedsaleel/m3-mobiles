# Django
from django.urls import path

# local Django
from . import views

app_name = 'userProfile'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my-addresses/', views.my_addresses, name='my-addresses')
]
