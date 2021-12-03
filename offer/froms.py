# Django
from django.forms import ModelForm, DateInput

# local
from .models import VariantOffer, ProductOffer, BrandOffer, Coupon


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


class CouponFrom(ModelForm):

    class Meta:
        model = Coupon
        fields = ['coupon_name', 'coupon_code', 'discount', 'limit', 'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': DateInput(attrs={'type': 'date'}),
            'valid_to': DateInput(attrs={'type': 'date'}),
        }
