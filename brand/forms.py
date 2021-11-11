# Django
from django.forms import ModelForm

# local Django
from .models import Brand


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'log']
