# Generated by Django 4.0.4 on 2022-05-27 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order_billing_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='countries',
            new_name='country',
        ),
    ]
