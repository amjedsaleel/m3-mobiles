# Generated by Django 3.2.9 on 2021-11-11 03:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
