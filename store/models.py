# Standard library
import uuid

# Django
from django.db import models

# local Django
from brand.models import Brand

# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    offer = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)


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
    # slug = models.SlugField(max_length=255, unique=True)
    stock = models.IntegerField()
    ram = models.CharField(max_length=20, choices=RAM)
    storage = models.CharField(max_length=20, choices=STORAGE)
    color = models.CharField(max_length=20, choices=COLOR)
    price = models.IntegerField()
    description = models.TextField(max_length=300)
    image1 = models.ImageField(upload_to='products')
    image2 = models.ImageField(upload_to='products', blank=True)
    image3 = models.ImageField(upload_to='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.product.name


