# Django
from django.forms import ModelForm

# local
from .models import VariantOffer, ProductOffer, BrandOffer


class VariantOfferForm(ModelForm):

    class Meta:
        model = VariantOffer
        fields = ['variant', 'discount_offer', 'is_active']


class ProductOfferForm(ModelForm):

    class Meta:
        model = ProductOffer
        fields = ['product', 'discount_offer', 'is_active']


class BrandOfferForm(ModelForm):

    class Meta:
        model = BrandOffer
        fields = ['brand', 'discount_offer', 'is_active']
