# django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'

urlpatterns = [
    # Signup, login, Sign out
    path('signup/', views.signup, name='signup'),
    path('login/', views.sign_in, name='sign-in'),
    path('sign-out/', views.log_out, name='sign-out'),

    # Verify account
    path('verifiy-account/', views.verify_account, name='verify-account'),

    # Login with OTP
    path('mobile-login/', views.mobile_login, name='mobile-login'),
    path('mobile-login-otp-verify/', views.mobile_login_otp_verify, name='mobile-login-otp-verify'),

    # Reset password
    path('reset-password/', views.reset_password, name='reset-password'),
    path('verify-reset-password-otp/', views.verify_reset_password_otp, name='verify-reset-password-otp'),
    path('set-new-password/', views.set_new_password, name='set-new-password'),

    path('resent-otp/', views.resent_otp, name='resent-otp')
]
