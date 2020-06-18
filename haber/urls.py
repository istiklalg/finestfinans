"""haber URL Configuration

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

from django.urls import path, re_path
from django.conf.urls import url
from haber.views import *

app_name = 'haber'          # href lerde url bağlantılarını belirtirken 'app name:url name' şeklinde yazacağız

urlpatterns = [
    path('lists/', haber_lists, name='lists'),
    path('index/', haber_index, name='index'),
    path('create/', haber_create, name='create'),
    path('about_us/', about_us, name='about_us'),
    path('kredi/', kredi_sec, name='kredi'),
    path('kredi_hesapla/', kredi_hesapla, name='hesapla'),
    re_path(r'^(?P<id>[\w-]+)/$', haber_detail, name='detail'),
    re_path(r'^(?P<id>[\w-]+)/update/', haber_update, name='update'),
    re_path(r'^(?P<id>[\w-]+)/delete/', haber_delete, name='delete'),


]
