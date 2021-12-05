# standard library
import uuid

# Django
from django.db import models

# local Django

# Create your models here.


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    log = models.ImageField(upload_to='brands')
    # offer = models.ForeignKey(BrandOffer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.lower()
        super().clean()

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Brand, self).save(*args, **kwargs)

    def get_products_count(self):
        return self.product_set.all().count()


