# Django
from django.db import models

# local Django
from brand.models import Brand
# Create your models here.


class BrandOffer(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, null=True, blank=True)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class ProductOffer(models.Model):
    product = models.OneToOneField('store.Product', on_delete=models.CASCADE, null=True, blank=True)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class VariantOffer(models.Model):
    variant = models.OneToOneField('store.Variant', on_delete=models.CASCADE, null=True, blank=True)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)

    def get_variant(self):
        variant = self.variant.slug
        return variant.replace("-", " ")
