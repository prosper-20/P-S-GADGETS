# Generated by Django 4.0.4 on 2022-06-27 15:50

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_userprofile_one_click_purchasing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='features',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
