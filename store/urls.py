# Django
from django.urls import path

# local Django
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store')
]