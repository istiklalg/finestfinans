"""budget URL Configuration

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
from budget.views import *

app_name = 'budget'          # href lerde url bağlantılarını belirtirken 'app name:url name' şeklinde yazacağız

urlpatterns = [
    path('index/', budget_index, name='index'),
    path('gruplar/', budget_groups, name='groups'),
    path('firmalar/', budget_companies, name='companies'),
    path('create/', budget_create, name='create'),
    path('compare/', budget_compare, name='compare'),

    re_path(r'^pdf/(?P<id>[\w-]+)/', budget_pdf, name='pdf'),

    re_path(r'^report/(?P<id>[\w-]+)/', budget_report, name='report'),



    re_path(r'^(?P<vergi>[\w-]+)/lists/', budget_lists, name='lists'),
    re_path(r'^(?P<id>[\w-]+)/$', budget_detail, name='detail'),
    re_path(r'^(?P<id>[\w-]+)/tablolar', budget_base_table, name='basetable'),
    re_path(r'^(?P<id>[\w-]+)/spread/', budget_spread, name='spread'),
    re_path(r'^(?P<id>[\w-]+)/update/', budget_update, name='update'),
    re_path(r'^(?P<id>[\w-]+)/delete/', budget_delete, name='delete'),
    re_path(r'^(?P<id>[\w-]+)/grupliste/', budget_group_list, name='grouplist'),
    re_path(r'^(?P<slug>[\w-]+)/grup_spread/', budget_group_spread, name='groupspread'),
    re_path(r'^(?P<slug>[\w-]+)/firmalar/', budget_groupfirms, name='groupfirms'),
    re_path(r'^(?P<id>[\w-]+)/analysis/', budget_analysis, name='analysis'),

]
