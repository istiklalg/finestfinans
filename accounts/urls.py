"""accounts URL Configuration

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
from django.contrib import admin
from django.conf.urls import url
from accounts.views import *

app_name = 'accounts'          # href lerde url bağlantılarını belirtirken 'app name:url name' şeklinde yazacağız

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('change_password/', password_change_view, name='change'),
    path('reset_password/', password_reset_view, name='reset'),
    path('info_update/', info_update_view, name='update'),
    path('logout/', logout_view, name='logout'),
    re_path('panel/', admin_view, name='admin'),
]
