# Generated by Django 4.0.4 on 2022-06-21 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_question_alter_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
