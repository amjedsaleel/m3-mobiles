# Generated by Django 3.2.9 on 2021-12-03 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0016_alter_redeemedcoupon_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='redeemedcoupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
