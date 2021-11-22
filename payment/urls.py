# Django
from django.urls import path

# local Django
from . import views

app_name = 'payments'

urlpatterns = [
    path('paypal/', views.paypal, name='paypal'),
    path('razorpay-payment-verification/', views.razorpay_payment_verification, name='razorpay-payment-verification')
]

