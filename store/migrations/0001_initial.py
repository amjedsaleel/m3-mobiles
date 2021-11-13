# Generated by Django 3.2.9 on 2021-11-13 06:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('offer', models.CharField(blank=True, max_length=30)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('stock', models.IntegerField()),
                ('ram', models.CharField(choices=[('2GB', '2GB'), ('4GB', '4GB'), ('8GB', '8GB'), ('12GB', '12GB')], max_length=20)),
                ('storage', models.CharField(choices=[('8GB', '8GB'), ('16GB', '16GB'), ('32GB', '32GB'), ('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB'), ('128GB', '128GB'), ('512GB', '512GB')], max_length=20)),
                ('color', models.CharField(choices=[('BLACK', 'BLACK'), ('BLUE', 'BLUE'), ('GREEN', 'GREEN'), ('WHITE', 'WHITE')], max_length=20)),
                ('price', models.IntegerField()),
                ('description', models.TextField(max_length=300)),
                ('image1', models.ImageField(upload_to='products')),
                ('image2', models.ImageField(blank=True, upload_to='products')),
                ('image3', models.ImageField(blank=True, upload_to='products')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
