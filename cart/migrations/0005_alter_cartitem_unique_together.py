# Generated by Django 3.2.9 on 2021-11-17 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]
