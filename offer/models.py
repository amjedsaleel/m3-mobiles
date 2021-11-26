from django.db import models


# Create your models here.


class BrandOffer(models.Model):
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class ProductOffer(models.Model):
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)


class VariantOffer(models.Model):
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)
