# Generated by Django 3.0.4 on 2020-04-06 13:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('haber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='haber',
            name='subtitle',
            field=ckeditor.fields.RichTextField(default=1, verbose_name='Haber Altbaşlığı'),
            preserve_default=False,
        ),
    ]