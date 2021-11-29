# Django
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# local Django
from . models import Coupon


@receiver(post_save, sender=Coupon)
def activate_coupon(sender, instance, created, *args, **kwargs):
    if created:
        if instance.valid_from == timezone.now().date():
            instance.is_active = True
            instance.save()
