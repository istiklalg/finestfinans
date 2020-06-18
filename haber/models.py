from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.


class Haber(models.Model):
    title = models.CharField(max_length=300, verbose_name='Haber Başlığı')
    subtitle = RichTextField(blank=True, verbose_name='Haber Altbaşlığı')
    content = RichTextField(blank=True, verbose_name='Haber İçeriği')
    publishing_date = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    images = models.ImageField(null=True, blank=True, verbose_name='Haberin Resmi')
    link = models.URLField(null=True, blank=True, verbose_name='Sayfa Yönlendirme İçin URL')
    konumlar = (('S', 'CAROUSEL-SLİDER'), ('M', 'MARKETING'), ('F', 'FEATURETTE'), ('H', 'HAKKIMIZDA'))
    konum = models.CharField(max_length=20, blank=True, choices=konumlar, verbose_name='Konumunu Seçin')
    position = models.IntegerField(blank=True, verbose_name='Yerleşim Sırası Seçin (0 ile başlar)')
    button = models.CharField(max_length=30, blank=True, verbose_name='Butonun Yazısı')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('haber:detail', kwargs={'id': self.id})

    def get_create_url(self):
        return reverse('haber:create')   # haber app sindeki create isimli url yi verdik,yeni nesne id yeni üretilecek

    def get_update_url(self):
        return reverse('haber:update', kwargs={'id': self.id})  # budget app sindeki update isimli url yi verdik

    def get_delete_url(self):
        return reverse('haber:delete', kwargs={'id': self.id})  # budget app sindeki delete isimli url yi verdik

    class Meta:
        ordering = ['-konum', 'position']

