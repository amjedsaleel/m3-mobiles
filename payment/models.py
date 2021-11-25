# Django
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    amount_paid = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_id
