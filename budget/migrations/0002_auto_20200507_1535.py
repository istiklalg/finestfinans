# Generated by Django 3.0.4 on 2020-05-07 12:35

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='comment1',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Dönen Varlık Kalemlerine İlişkin Tespitler ve Yorumlar:'),
        ),
        migrations.AddField(
            model_name='budget',
            name='comment2',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Duran Varlık Kalemlerine İlişkin Tespitler ve Yorumlar:'),
        ),
        migrations.AddField(
            model_name='budget',
            name='comment3',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Yabancı Kaynaklar Kalemlerine İlişkin Tespitler ve Yorumlar:'),
        ),
        migrations.AddField(
            model_name='budget',
            name='comment4',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Özkaynak Kalemlerine İlişkin Tespitler ve Yorumlar:'),
        ),
        migrations.AddField(
            model_name='budget',
            name='comment5',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Gelir Tablosuna İlişkin Tespitler ve Yorumlar:'),
        ),
        migrations.AddField(
            model_name='budget',
            name='comment6',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Oran Analizine İlişkin Tespitler ve Yorumlar:'),
        ),
    ]