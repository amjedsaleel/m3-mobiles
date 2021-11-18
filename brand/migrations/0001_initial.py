# Generated by Django 3.2.9 on 2021-11-18 10:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('log', models.ImageField(upload_to='brands')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
