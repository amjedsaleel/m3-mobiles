# Django
from django import forms

# local Django
from .models import Variant, Product


class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['product', 'stock', 'ram', 'storage', 'color', 'description', 'landing_price', 'mrp', 'image1',
                  'image2', 'image3']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'name']
