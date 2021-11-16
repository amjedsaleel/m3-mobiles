# Django
from django.db import models

# local Django
from store.models import Variant

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cart} + {self.variant}'

    def sub_total(self):
        return self.variant.price * self.quantity

