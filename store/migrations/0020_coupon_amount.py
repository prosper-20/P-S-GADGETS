# Generated by Django 4.0.4 on 2022-05-31 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]
