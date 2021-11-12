# Django
from django.forms import ModelForm

# local Django
from .models import Variant, Product


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ['product', 'stock', 'ram', 'storage', 'color', 'price', 'description', 'image1', 'image2',
                  'image3']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'name']
