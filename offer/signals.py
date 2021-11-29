# Django
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

# local Django
from . models import Coupon


@receiver(pre_save, sender=Coupon)
def activate_coupon(sender, instance, *args, **kwargs):

    if instance.valid_from == timezone.now().date():
        instance.is_active = True
