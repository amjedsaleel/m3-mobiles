# Django
from django import forms

# local Django
from .models import Address
from django.contrib.auth import get_user_model


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'email', 'house_no', 'area', 'landmark', 'town', 'state', 'pin', 'type']


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'mobile']
