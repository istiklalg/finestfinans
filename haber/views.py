
import datetime
import locale
from haber.forms import *
from django.db.models import Q
from haber.models import Haber
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.
locale.setlocale(locale.LC_ALL, locale='tr_TR.utf8')


def haber_index(request):
    global bilgi1, bilgi2, bilgi3, bilgi4, bilgi5, bilgi6, bilgi7, bilgi8, bilgi9, about_us, bilgi11, bilgi12, kisi
    haberler = Haber.objects.all()

    saat = datetime.datetime.strftime(datetime.datetime.today(), '%H:%M')
    today = datetime.datetime.strftime(datetime.datetime.today(), '%d %b %Y')
    if request.user.is_authenticated:
        kisi = request.user.username
    else:
        kisi = 'Misafir'
    print('*****Anasayfa ', today, ' saat', saat, '--', kisi)
    # print('*****II- ', request.META['COMPUTERNAME'], '- kullanıcı --', request.META['USERNAME'],
    #       '--', request.META['HTTP_X_REAL_IP'])
    # print('*****III- ')

    def diz(haber):
        return haber.position

    try:
        S = [haber for haber in haberler if haber.konum == 'S']
        M = [haber for haber in haberler if haber.konum == 'M']
        F = [haber for haber in haberler if haber.konum == 'F']
        H = [haber for haber in haberler if haber.konum == 'H']
        S.sort(key=diz)
        M.sort(key=diz)
        F.sort(key=diz)
        H.sort(key=diz)
        # print('SLIDER', S)
        # print('MARKETING', M)
        # print('FEATURETTE', F)
        # print('HAKKIMIZDA', H)
    except Exception as err:
        print('**** -', err)
        messages.info(request, 'Kaynak silinmiş olmalı, en kısa sürede sorunu gidereceğiz.')

    query = request.GET.get('q')
    if query:
        haberler = haberler.filter(Q(title__icontains=query) |
                                   Q(subtitle__icontains=query) |
                                   Q(content__icontains=query) |
                                   Q(publishing_date__icontains=query)).distinct()
        context = {
            'query': query, 'today': today,
            'haberler': haberler
        }
        return render(request, 'haber/index.html', context)
    context = {
        'haberler': haberler, 'today': today,
        'S': S, 'M': M, 'F': F, 'H': H,
    }
    return render(request, 'home.html', context)


def haber_lists(request):  # Eksik!!!!!!!
    # aktif_kisi = request.user
    # print(aktif_kisi)
    # s = requests.Session()
    # class MyAuth(requests.auth.AuthBase):
    #     def __call__(self, r):
    #         return r
    # # print(s)
    # # print('haber_lists içeriği çalıştı, bağlantı kurmaya çalışıyor')
    # r = s.get("http://127.0.0.1:8000/budget/9/spread")
    # print(r)
    # soup = BeautifulSoup(r.content, "html.parser")
    # tablo1 = soup.find_all('table')
    # # print(soup.prettify())
    # # for i in tablo1:
    # #     print('tablo1 listesi {} içerik'.format(i))
    # context = {
    #     'icerik': soup.prettify(),
    #     'tablo': tablo1
    # }
    # return render(request, 'haber/index.html', context)
    return redirect('home')


def haber_detail(request, id):
    haber = get_object_or_404(Haber, id=id)
    context = {
        'haber': haber
    }
    return render(request, 'haber/detail.html', context)


def haber_create(request):
    if not request.user.is_superuser:  # bu if koşulu ile kullanıcı süper değilse 404 sayfası gönderir
        messages.error(request, 'Yetkili olmadığınız bir giriş deniyorsunuz!')
        return redirect('budget:index')
    form = AddHaber(request.POST or None, request.FILES or None)
    if form.is_valid():
        haber = form.save(commit=False)
        haber.save()
        print('***** Yayının konumu :', haber.konum, '--', haber.position)
        messages.success(request, 'Yeni haber kaydedilmiştir, haber id : {}'.format(haber.id))
        return HttpResponseRedirect(haber.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'haber/form.html', context)


def haber_update(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'Yetkili olmadığınız bir giriş deniyorsunuz!')
        return redirect('budget:index')
    haber = get_object_or_404(Haber, id=id)  # id si gelen nesneyi alıp haber değişkenine tanımlıyorum
    form = AddHaber(request.POST or None, request.FILES or None, instance=haber)
    if form.is_valid():  # üst satırda get object ile çektiğim formu instance ile formun içine atıyorum
        form.save()
        print('***** Yayının konumu :', haber.konum, '--', haber.position)
        messages.success(request, 'Yaptığınız düzenlemeler kaydedilmiştir.')
        return HttpResponseRedirect(haber.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'haber/form.html', context)


def haber_delete(request, id):
    if not request.user.is_superuser:  # bu if koşulu ile kullanıcı girişi yapılmamışsa 404 sayfası gönderir
        messages.error(request, 'Yetkili olmadığınız bir giriş deniyorsunuz!')
        return redirect('budget:index')

    haber = get_object_or_404(Haber, id=id)
    haber.delete()
    print('***** YAYIN SİLİNDİ :', haber.id, '--', haber.title, '--', haber.konum, '--', haber.position)
    messages.error(request, "UYARI : {} id'li haber içeriği silinmiştir!!  Bu değişiklik anasayfada sorun yaratabilir")
    return redirect('accounts:admin')


def about_us(request):
    try:
        haberler = Haber.objects.all()
    except ObjectDoesNotExist or MultipleObjectsReturned:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('home')

    if request.user.is_authenticated:
        kisi = request.user.username
        print('*****Hakkımızda : ', kisi)
    else:
        kisi = 'Misafir'
        print('*****Hakkımızda : ', kisi)

    def diz(haber):
        return haber.position
    try:
        biz = [haber for haber in haberler if haber.konum == 'H']
        biz.sort(key=diz)
    except Exception as err:
        print('**** -', err)
        messages.info(request, 'Kaynak silinmiş olmalı, en kısa sürede sorunu gidereceğiz.')

    return render(request, 'haber/detail.html', {'biz': biz})


def kredi_sec(request):
    data = 'hesaplayın'
    liste = ['Bireysel Kredi', 'Ticari Kredi']
    bireysel = ['Konut', 'İhtiyaç', 'Taşıt']
    ticari = ['Taksitli Ticari', 'İşyeri', 'Ticari Taşıt', 'İskonto', 'Spot']
    secim = request.POST.get('kredi_tipi')
    print('İlk seçim : ', secim)
    if secim and secim == 'Bireysel Kredi':
        liste = bireysel
        secim = request.POST.get('kredi_tipi')
        print('İkinci Seçim - Bireysel : ', secim)
    elif secim and secim == 'Ticari Kredi':
        liste = ticari
        secim = request.POST.get('kredi_tipi')
        print('İkinci Seçim - Ticari: ', secim)

    if secim in {'Konut', 'İhtiyaç', 'Taşıt', 'Taksitli Ticari', 'İşyeri', 'Ticari Taşıt'}:
        form = TaksitliForm(data={'tip': secim})
    elif secim == 'İskonto':
        form = TaksitliForm(data={'tip': secim})
    elif secim == 'Spot':
        form = TaksitliForm(data={'tip': secim})
    else:
        form = None

    context = {
        'data': data, 'liste': liste, 'secim': secim, 'form': form
    }
    return render(request, 'haber/kredi.html', context)


def kredi_hesapla(request):

    def kredi(tipi, tutar, faiz, vade):
        global kkdf, bsmv
        if tipi == 'Spot':
            kkdf, bsmv = 0, 5
            f = (faiz / 100) * ((100 + kkdf + bsmv) / 100)
            odenen_faiz = round((tutar * faiz * vade / 36000), 2)
            odenen_bsmv = round((odenen_faiz * bsmv / 100), 2)
            geri_odeme = round((tutar + odenen_faiz + odenen_bsmv), 2)
            odeme_tarihi = datetime.datetime.strftime((datetime.datetime.today() +
                                                       datetime.timedelta(days=vade)), '%d %B %Y')
            plan = [(tutar, odeme_tarihi, odenen_faiz, odenen_bsmv, geri_odeme)]
            return plan

        elif tipi == 'İskonto':
            kkdf, bsmv = 0, 5
            f = (faiz / 100) * ((100 + kkdf + bsmv) / 100)
            odenen_faiz = round((tutar * faiz * vade / 36000), 2)
            odenen_bsmv = round((odenen_faiz * bsmv / 100), 2)
            odeme_tarihi = datetime.datetime.strftime((datetime.datetime.today() +
                                                       datetime.timedelta(days=vade)), '%d %B %Y')
            iskonto = round((tutar - odenen_faiz - odenen_bsmv), 2)
            plan = [(iskonto, odeme_tarihi, odenen_faiz, odenen_bsmv, tutar)]

            return plan

        elif tipi in ['İhtiyaç', 'Taşıt']:
            kkdf, bsmv = 15, 5
        elif tipi == 'Konut':
            kkdf, bsmv = 0, 0
        elif tipi in ['Taksitli Ticari', 'İşyeri', 'Ticari Taşıt']:
            kkdf, bsmv = 0, 5

        f = (faiz / 100) * ((100 + kkdf + bsmv) / 100)
        taksit = tutar * ((f * ((1 + f) ** vade)) / (((1 + f) ** vade) - 1))
        tarih = datetime.datetime.strftime(datetime.datetime.now(), '%d %B %Y')
        plan = []
        toplam_taksit = toplam_faiz = toplam_kkdf = toplam_bsmv = odenen_anapara = 0
        for i in range(1, vade + 1):
            plan.append((i,
                         datetime.datetime.strftime((datetime.datetime.today() +
                                                     datetime.timedelta(days=i * 30.5)), '%d %B %Y'),
                         round(taksit, 2),
                         round((tutar * faiz / 100), 2), round((tutar * faiz * kkdf / 10000), 2),
                         round((tutar * faiz * bsmv / 10000), 2),
                         round((taksit - (tutar * faiz / 100) - (tutar * faiz * kkdf / 10000) -
                                (tutar * faiz * bsmv / 10000)), 2),
                         round((tutar - (taksit - (tutar * faiz / 100) - (tutar * faiz * kkdf / 10000) -
                                         (tutar * faiz * bsmv / 10000))), 2)))
            tutar = (tutar - (taksit - (tutar * faiz / 100) - (tutar * faiz * kkdf / 10000) -
                              (tutar * faiz * bsmv / 10000)))
        for i in range(0, len(plan)):
            toplam_taksit = toplam_taksit + plan[i][2]
            toplam_faiz = toplam_faiz + plan[i][3]
            toplam_kkdf = toplam_kkdf + plan[i][4]
            toplam_bsmv = toplam_bsmv + plan[i][5]
            odenen_anapara = odenen_anapara + plan[i][6]
        plan.append(('Toplam', ' ', round(toplam_taksit, 2), round(toplam_faiz, 2), round(toplam_kkdf, 2),
                     round(toplam_bsmv, 2), round(odenen_anapara, 2), ' '))

        return plan

    tipi = request.POST.get('tip')
    if tipi not in ['Konut', 'İhtiyaç', 'Taşıt', 'Taksitli Ticari', 'İşyeri', 'Ticari Taşıt', 'İskonto', 'Spot']:
        print(f'***** Seçilen kredi türü ile oynanmış değer : {tipi}')
        messages.warning(request, 'Lütfen seçilen kredi türü alanını değiştirmeyiniz!')
        return redirect('haber:kredi')
    tutar = float(request.POST.get('tutar'))
    faiz = float(request.POST.get('faiz'))
    vade = int(request.POST.get('vade'))
    print('Hesapla view : ', tipi)

    plan = kredi(tipi, tutar, faiz, vade)

    if tipi == 'Spot':
        data = '{} TL, {} gün vadeli yıllık %{} faiz oranı ile {} kredi detayları :'.format(tutar, vade, faiz, tipi)
    elif tipi == 'İskonto':
        data = '{} TL, {} gün vadeli alacak için yıllık %{} faiz oranı ile {} detayı :'.format(tutar, vade, faiz, tipi)
    else:
        data = '{} TL, aylık %{} faiz oranı ile {} ay vadeli {} için ödeme planı :'.format(tutar, faiz, vade, tipi)

    context = {
        'tipi': tipi,
        'data': data,
        'odeme_plan': plan,
    }

    return render(request, 'haber/tablo.html', context)

