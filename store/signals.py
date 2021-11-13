# Django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# local Django
from .models import Product, Variant


@receiver(pre_save, sender=Product)
def create_product_slug(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Variant)
def create_variant_slug(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(f'{instance.product.name} {instance.color} {instance.ram} {instance.storage}')
