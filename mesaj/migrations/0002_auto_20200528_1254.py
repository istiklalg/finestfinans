# Generated by Django 3.0.4 on 2020-05-28 09:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mesaj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesaj',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Mesaj İçeriği'),
        ),
    ]
