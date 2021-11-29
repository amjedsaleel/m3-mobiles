# Django
from django.urls import path

# local Django
from . import views

app_name = 'offers'

urlpatterns = [
    path('apply-coupon/', views.apply_coupon, name='apply-coupon'),
]
