# Generated by Django 3.2.9 on 2021-11-25 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
        ('store', '0003_remove_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.productoffer'),
        ),
        migrations.AddField(
            model_name='variant',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.variantoffer'),
        ),
    ]
