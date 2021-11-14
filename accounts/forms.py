# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    """
    User SignUp form
    """
    password1 = forms.CharField(label='Password', required=True,
                                widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'mobile']


class ResetPasswordForm(forms.Form):
    """
    Password reset form
    """
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        password1 = self.cleaned_data.get("new_password")
        password2 = self.cleaned_data.get("confirm_password")

        if password1 != password2:
            self.add_error('confirm_password', 'Passwords is not matching')

        try:
            password_validation.validate_password(password=password1)
        except ValidationError as error:
            self.add_error('confirm_password', error)

        return cleaned_data
