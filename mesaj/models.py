
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your models here.


class Mesaj(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50, verbose_name='Kullanıcı Adı / '
                                                               '(Kayıtlı kullanıcı değilseniz Ad Soyad giriniz)')
    email = models.EmailField(max_length=50, verbose_name='e-posta adresiniz')
    title = models.CharField(max_length=300, verbose_name='Mesaj Konusu (Mesajınız ne ile ilgili?)')
    content = RichTextField(blank=True, verbose_name='Mesaj İçeriği')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    files = models.FileField(null=True, blank=True, verbose_name='Konuya ilişkin eklemek istediğiniz belge varsa ekleyin')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mesaj:detail', kwargs={'id': self.id})

    def get_create_url(self):
        return reverse('mesaj:create')   # haber app sindeki create isimli url yi verdik,yeni nesne id yeni üretilecek

    def get_update_url(self):
        return reverse('mesaj:update', kwargs={'id': self.id})  # budget app sindeki update isimli url yi verdik

    def get_delete_url(self):
        return reverse('mesaj:delete', kwargs={'id': self.id})  # budget app sindeki delete isimli url yi verdik

    class Meta:
        ordering = ['-date', '-id']


