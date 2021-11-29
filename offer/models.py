# standard library
import uuid

# Django
from django.db import models
from django.contrib.auth import get_user_model

# local Django
from brand.models import Brand

# Create your models here.


class BrandOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class ProductOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField('store.Product', on_delete=models.CASCADE)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class VariantOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.OneToOneField('store.Variant', on_delete=models.CASCADE)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)

    def get_variant(self):
        variant = self.variant.slug
        return variant.replace("-", " ")


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Offer in percentage", null=True)
    limit = models.PositiveIntegerField()
    used = models.PositiveIntegerField(default=0, editable=False)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_name


class RedeemedCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)


