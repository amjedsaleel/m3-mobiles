# Generated by Django 3.2.9 on 2021-12-06 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coupon_name', models.CharField(max_length=50)),
                ('coupon_code', models.CharField(max_length=50, unique=True)),
                ('discount', models.PositiveIntegerField(help_text='Offer in percentage', null=True)),
                ('limit', models.PositiveIntegerField()),
                ('used', models.PositiveIntegerField(default=0)),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VariantOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_offer', models.PositiveIntegerField(help_text='Offer in percentage')),
                ('is_active', models.BooleanField(default=True)),
                ('variant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.variant')),
            ],
        ),
        migrations.CreateModel(
            name='RedeemedCoupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.coupon')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_offer', models.PositiveIntegerField(help_text='Offer in percentage')),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='BrandOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_offer', models.PositiveIntegerField(help_text='Offer in percentage')),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
    ]
