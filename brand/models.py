# standard library
import uuid

# Django
from django.db import models

# Create your models here.


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    log = models.ImageField(upload_to='brands')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
