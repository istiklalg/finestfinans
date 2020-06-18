
import datetime
from django.shortcuts import render, HttpResponse
# import requests
# from bs4 import BeautifulSoup

# Create your views here.


def home_view(request):
    # print('home_view çalıştı')
    # r = requests.get("https://altinkaynak.com")
    # soup = BeautifulSoup(r.content, "html.parser")
    # tablo1 = soup.find_all("div", {"id": "cphMain_upCurrency"})
    # print(tablo1)
    today = datetime.datetime.today()
    print(today)

    if request.user.is_authenticated:
        context = {
            'isim': 'İstiklal',
            'today': today
        }
    else:
        context = {
            'isim': 'Misafir',
            'today': today
        }

    return render(request, 'home.html', context)

