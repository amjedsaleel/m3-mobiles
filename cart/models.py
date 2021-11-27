# Django
from django.db import models
from django.contrib.auth import get_user_model

# local Django
from store.models import Variant

User = get_user_model()

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'variant', )

    def __str__(self):
        return f'{self.cart} + {self.variant}'

    def sub_total(self):
        price = self.variant.get_price()
        return price['price'] * self.quantity

