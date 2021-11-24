# standard library
from datetime import datetime
import random

# Django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import IntegrityError

# local Django
from .models import OrderProduct


@receiver(pre_save, sender=OrderProduct)
def oder_number(sender, instance, *args, **kwargs):

    if not instance.tracking_id:
        random_number = random.randint(0, 9)
        instance.tracking_id = f'TR{random_number}-{datetime.now().strftime("%Y%m%d%H%M%S")}'
