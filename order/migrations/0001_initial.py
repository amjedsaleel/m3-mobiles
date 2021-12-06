# Generated by Django 3.2.9 on 2021-12-06 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('full_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('house_no', models.CharField(max_length=255, verbose_name='House no/Building/Company')),
                ('area', models.CharField(max_length=255, verbose_name='Area/Street/Sector/Village')),
                ('landmark', models.CharField(blank=True, max_length=50)),
                ('town', models.CharField(max_length=50, verbose_name='Town/City')),
                ('state', models.CharField(max_length=50)),
                ('pin', models.PositiveIntegerField()),
                ('order_total', models.FloatField()),
                ('tax', models.FloatField()),
                ('grand_total', models.FloatField(null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.payment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tracking_id', models.CharField(editable=False, max_length=50, null=True, unique=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Out of Delivery', 'Out of Delivery'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='New', max_length=50)),
                ('quantity', models.IntegerField()),
                ('paid', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variant')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
