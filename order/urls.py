# Django
from django.urls import path

# local Django
from . import views

app_name = 'order'

urlpatterns = [
    path('place-order/', views.place_order, name='place-order')
]
