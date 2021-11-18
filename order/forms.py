# Django
from django.forms import ModelForm

# local Django
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'house_no', 'area', 'landmark', 'town', 'state', 'pin']
