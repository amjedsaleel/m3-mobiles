# Standard library
import uuid

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum

# local Django
from brand.models import Brand
from offer.models import VariantOffer


# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    # offer = models.ForeignKey(ProductOffer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)

    def get_count(self):
        """
        Get total count of variants under this product
        """
        return self.variant_set.all().count()


RAM = (
    ('2GB', '2GB'),
    ('4GB', '4GB'),
    ('8GB', '8GB'),
    ('12GB', '12GB'),
)

STORAGE = (
    ('8GB', '8GB'),
    ('16GB', '16GB'),
    ('32GB', '32GB'),
    ('64GB', '64GB'),
    ('128GB', '128GB'),
    ('256GB', '256GB'),
    ('128GB', '128GB'),
    ('512GB', '512GB'),
)

COLOR = (
    ('BLACK', 'BLACK'),
    ('BLUE', 'BLUE'),
    ('GREEN', 'GREEN'),
    ('WHITE', 'WHITE'),
)


class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    stock = models.IntegerField()
    ram = models.CharField(max_length=20, choices=RAM)
    storage = models.CharField(max_length=20, choices=STORAGE)
    color = models.CharField(max_length=20, choices=COLOR)
    landing_price = models.IntegerField(verbose_name="Landing price", null=True)
    mrp = models.IntegerField(verbose_name='M.R.P', null=True)
    tax = models.IntegerField(null=True)
    description = models.TextField(max_length=300)
    # offer = models.ForeignKey(VariantOffer, on_delete=models.SET_NULL, blank=True, null=True)
    image1 = models.ImageField(upload_to='products')
    image2 = models.ImageField(upload_to='products', blank=True)
    image3 = models.ImageField(upload_to='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'ram', 'storage', 'color',)

    def __str__(self):
        return self.slug

    def clean(self):
        super().clean()
        self.landing_price = self.landing_price
        self.mrp = self.mrp

        if not self.mrp > self.landing_price:
            raise ValidationError("M.R.P must be higher than landing price")

    def get_variant(self):
        return f'{self.ram} RAM, {self.storage} Storage, {self.color}'

    def get_price(self):
        try:
            if self.variantoffer.is_active:
                offer_price = (self.mrp / 100) * self.variantoffer.discount_offer
                price = self.mrp - offer_price
                return {'price': price, 'discount': self.variantoffer.discount_offer}
            raise
        except:
            try:
                if self.product.productoffer.is_active:
                    offer_price = (self.mrp / 100) * self.product.productoffer.discount_offer
                    price = self.mrp - offer_price
                    return {'price': price, 'discount': self.product.productoffer.discount_offer}
                raise
            except:
                try:
                    if self.product.brand.brandoffer.is_active:
                        offer_price = (self.mrp / 100) * self.product.brand.brandoffer.discount_offer
                        price = self.mrp - offer_price
                        return {'price': price, 'discount': self.product.brand.brandoffer.discount_offer}
                    raise
                except:
                    pass
                return {'price': self.mrp}

    def sold_count(self):
        result = self.orderproduct_set.filter(status='Delivered').aggregate(Sum('quantity'))
        sold = str(result['quantity__sum'])
        return sold.replace('None', '0')

    def get_revenue(self):
        result = self.orderproduct_set.filter(status='Delivered').aggregate(Sum('paid'))
        revenue = str(result['paid__sum'])
        return revenue.replace('None', '0')

    def get_profit(self):
        quantity = self.orderproduct_set.filter(variant=self, status='Delivered').aggregate(Sum('quantity'))
        paid = self.orderproduct_set.filter(variant=self, status='Delivered').aggregate(Sum('paid'))
        profit = float(str(paid['paid__sum']).replace('None', '0')) - self.landing_price * float(
            str(quantity['quantity__sum']).replace('None', '0'))
        return profit


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rating
