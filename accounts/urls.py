# django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.sign_in, name='sign-in'),
    path('sign-out/', views.log_out, name='sign-out'),
    path('verifiy-account/', views.verify_account, name='verify-account'),
    path('verify-otp/', views.verity_opt, name='verify-otp'),

]