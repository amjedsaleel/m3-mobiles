# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'mobile']
