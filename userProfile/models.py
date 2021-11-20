# standard library
import uuid

# Django
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    house_no = models.CharField(max_length=255, verbose_name='House no/Building/Company')
    area = models.CharField(max_length=255, verbose_name='Area/Street/Sector/Village')
    landmark = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50, verbose_name='Town/City')
    state = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()
    type = models.CharField(max_length=50, verbose_name='Address Type', help_text='Example:- Home, Office, etc',
                            null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
