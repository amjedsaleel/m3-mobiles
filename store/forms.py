# Django
from django.forms import ModelForm

# local Django
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'name', 'stock', 'ram', 'storage', 'color', 'price', 'description', 'image1', 'image2',
                  'image3']
