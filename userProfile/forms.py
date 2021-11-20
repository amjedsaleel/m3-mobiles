# Django
from django import forms

# local Djnago
from .models import Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'email', 'house_no', 'area', 'landmark', 'town', 'state', 'pin', 'type']
