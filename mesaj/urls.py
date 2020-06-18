"""mesaj URL Configuration

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
from mesaj.views import *

app_name = 'mesaj'          # href lerde url bağlantılarını belirtirken 'app name:url name' şeklinde yazacağız

urlpatterns = [
    path('index/', mesaj_index, name='index'),
    path('create/', mesaj_create, name='create'),
    re_path(r'^(?P<id>[\w-]+)/$', mesaj_detail, name='detail'),
    re_path(r'^(?P<id>[\w-]+)/update/', mesaj_update, name='update'),
    re_path(r'^(?P<id>[\w-]+)/delete/', mesaj_delete, name='delete'),

#     path('spread/', budget_spread, name='spread'),
#     path('analysis/', budget_analysis, name='analysis'),
#     path('report/', budget_report, name='report'),
#     path('compare/', budget_compare, name='compare'),
#     path('comparison/', budget_comparison, name='comparison'),
# #   path('detail/', budget_detail, name='detail'),
#     re_path(r'^(?P<vergi>[\w-]+)/lists/', budget_lists, name='lists'),

#

]
