# Django
from django.urls import path

# local Django
from . import views

app_name = 'payments'

urlpatterns = [
    path('paypal/', views.paypal, name='paypal'),
    path('razorpay-payment-verification/', views.razorpay_payment_verification, name='razorpay-payment-verification'),
    path('failed/', views.failed, name='payment-failed'),
    path('cash-on-delivery-confirmation/', views.cod_confirmation, name='cod-confirmation'),
    path('cash-on-delivery/', views.cash_on_delivery, name='cash-on-delivery'),
]
