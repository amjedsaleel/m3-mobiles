# Generated by Django 3.2.9 on 2021-11-27 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_orderproduct_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='price',
            new_name='paid',
        ),
    ]