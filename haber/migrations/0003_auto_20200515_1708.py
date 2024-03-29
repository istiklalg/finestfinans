# Generated by Django 3.0.4 on 2020-05-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haber', '0002_haber_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='haber',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Sayfa Yönlendirme İçin URL'),
        ),
        migrations.AlterField(
            model_name='haber',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Haberin Resmi'),
        ),
    ]
