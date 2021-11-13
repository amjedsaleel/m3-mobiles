# Django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# local Django
from .models import Brand


@receiver(pre_save, sender=Brand)
def create_brand_slug(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.name)
