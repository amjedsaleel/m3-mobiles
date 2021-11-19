# Django
from django.urls import path

# local Django
from . import views

app_name = 'payments'

urlpatterns = [
    path('paypal/', views.paypal, name='paypal')
]

