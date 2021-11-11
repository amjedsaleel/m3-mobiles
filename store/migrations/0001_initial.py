# Generated by Django 3.2.9 on 2021-11-11 04:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0002_alter_brand_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('stock', models.IntegerField()),
                ('description', models.TextField(max_length=300)),
                ('image1', models.ImageField(upload_to='products')),
                ('image2', models.ImageField(upload_to='products')),
                ('image3', models.ImageField(upload_to='products')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
    ]
