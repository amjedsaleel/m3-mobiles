# django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.sign_in, name='sign-in')
]