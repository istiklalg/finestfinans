"""companybudgets URL Configuration  -- Projenin çatı url configürasyonu bu kısımda yer almaktadır.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('companybudgets/', include('companybudgets.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from home.views import home_view
from haber.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='django_admin'),
    path('', haber_index, name='home'),
    path('bilanco/', include('budget.urls')),  # budget app si için budgets'in içindeki urls.py yi adres gösterdik
    path('accounts/', include('accounts.urls')),  # accountst app si için oranın içindeki urls.py yi adres gösterdik
    path('haber/', include('haber.urls')),  # haber app si için kendi içindeki urls.py yi adres gösterdik
    path('mesaj/', include('mesaj.urls')),  # mesaj app si için kendi içindeki urls.py yi adres gösterdik
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
