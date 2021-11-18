# Standard
import uuid

# Django
from django.db import models
from django.contrib.auth import get_user_model

# local Django
from payment.models import Payment
from cart.models import Variant

# Create your models here.

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    house_no = models.CharField(max_length=255, verbose_name='House no/Building/Company')
    area = models.CharField(max_length=255, verbose_name='Area/Street/Sector/Village')
    landmark = models.CharField(max_length=50)
    town = models.CharField(max_length=50, verbose_name='Town/City')
    state = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()
    order_total = models.FloatField()
    tax = models.FloatField()
    grand_total = models.FloatField(null=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variant.slug
