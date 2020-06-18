
import csv
import datetime
import locale

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from django.utils.text import slugify
from django.contrib.auth.models import User, UserManager, Group, Permission

from budget.forms import *
from budget.mizan import *

# Create your views here.
locale.setlocale(locale.LC_ALL, locale='tr_TR.utf8')


def budget_groups(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    query = request.GET.get('q')
    if query:
        budgets = budgets.filter(Q(tax_title__icontains=query) |
                                 Q(tax_number__icontains=query) |
                                 Q(period__icontains=query) |
                                 Q(grup_ismi__icontains=query)).distinct()
    gruplar = [budget for budget in budgets if budget.grup_ismi]
    grup_isimleri = list(set([budget.grup_ismi for budget in gruplar]))
    firma_isimleri = list(set([budget.tax_title for budget in gruplar]))
    firma_vkn = list(set([budget.tax_number for budget in gruplar]))
    print('***** Gruplar Listesi : ', aktif_kisi.username, '--', grup_isimleri)
    # print(firma_isimleri, firma_vkn)
    grup_firma = []
    for a in grup_isimleri:
        grup_firma.append([budget for budget in gruplar if budget.grup_ismi == a])
    sample = [liste[0] for liste in grup_firma]
    # print(sample)
    note = f'{len(grup_isimleri)} FARKLI GRUP VE BU GRUPLAR İÇİNDE {len(firma_vkn)} FARKLI FİRMA TANIMLAMANIZ BULUNMAKTADIR.'
    if len(gruplar) == 0:
        note = 'GİRDİĞİNİZ MALİ VERİLERDE GRUP TANIMLAMASI BULUNMAMAKTADIR.'
    # print('***** Grup Listesi : ', aktif_kisi.username, '--', request.META['HTTP_X_REAL_IP'])   # sunucuda açılacak
    paginator = Paginator(sample, 10)  # Sayfa başına nesne sayısı 10
    page = request.GET.get('page')  # Sayfa tanımlaması,
    try:
        sample = paginator.page(page)
    except PageNotAnInteger:
        sample = paginator.page(1)
    except EmptyPage:
        sample = paginator.page(paginator.num_pages)

    context = {
        'budgets': gruplar, 'sample': sample, ''
        'note': note,
    }
    return render(request, 'budget/gruplar.html', context)


def budget_groupfirms(request, slug):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    grup = [budget for budget in budgets if slugify(budget.grup_ismi) == slug]
    numlist = list(set([budget.tax_number for budget in grup]))
    firmalar = []
    for number in numlist:
        firmalar.append([budget for budget in grup if budget.tax_number == number])
    sample = [liste[0] for liste in firmalar]
    total_count = len(numlist)
    group_name = sample[0].grup_ismi
    note = f'{group_name} ŞİRKETLER GRUBUNA TANIMALANMIŞ OLAN {total_count} ADET FİRMA VARDIR.'
    print('***** Grubun Firmalar Listesi : ', aktif_kisi.username, '--', slug, '--', numlist)
    paginator = Paginator(sample, 10)  # Sayfa başına nesne sayısı 10
    page = request.GET.get('page')  # Sayfa tanımlaması,
    try:
        sample = paginator.page(page)
    except PageNotAnInteger:
        sample = paginator.page(1)
    except EmptyPage:
        sample = paginator.page(paginator.num_pages)

    context = {
        'budgets': budgets, 'sample': sample,
        'note': note,
    }
    return render(request, 'budget/firmalar.html', context)


def budget_companies(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    query = request.GET.get('q')
    if query:
        budgets = budgets.filter(Q(tax_title__icontains=query) |
                                 Q(tax_number__icontains=query) |
                                 Q(period__icontains=query) |
                                 Q(grup_ismi__icontains=query)).distinct()
    total_count = len(budgets)
    firma_isimleri = list(set([budget.tax_title for budget in budgets]))
    firma_vkn = list(set([budget.tax_number for budget in budgets]))
    print('***** Firmalar Listesi : ', aktif_kisi.username, '--', firma_isimleri)
    # print(firma_isimleri, firma_vkn)
    if len(firma_isimleri) != len(firma_vkn):
        print(f'***** Kayıtlarda hata var! -- VKN sayısı : {len(firma_vkn)}, Unvan sayısı : {len(firma_isimleri)}')
        messages.warning(request, 'Kayıtlarınız arasında VKN ile ÜNVAN uyumsuzluğu olanlar var, '
                                        'vergi numarası aynı olan firmaların ünvanları da birebir aynı olmalıdır !')
    firma = []
    for number in firma_vkn:
        firma.append([budget for budget in budgets if budget.tax_number == number])
    # print(firma)
    sample = [liste[0] for liste in firma]
    # print(sample)
    note = f'{len(firma_vkn)} FARKLI FİRMA TANIMLAMANIZ BULUNMAKTADIR, TOPLAM KAYITLARINIZ {total_count} ADETTİR'
    if not query and len(budgets) == 0:
        note = 'GİRDİĞİNİZ MALİ VERİ BULUNMAMAKTADIR.'

    paginator = Paginator(sample, 10)  # Sayfa başına nesne sayısı 10
    page = request.GET.get('page')  # Sayfa tanımlaması,
    try:
        sample = paginator.page(page)
    except PageNotAnInteger:
        sample = paginator.page(1)
    except EmptyPage:
        sample = paginator.page(paginator.num_pages)

    context = {
        'budgets': budgets, 'sample': sample,
        'note': note,
    }
    return render(request, 'budget/firmalar.html', context)


def budget_index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    # print('***** Index ', aktif_kisi.username, '--', request.META['HTTP_X_REAL_IP'])   # sunucuda açılacak
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    query = request.GET.get('q')   # arama çubuğunun boş olup olmadığını kontrol ediyoruz, dolu ise arama başlatıyoruz.
    if query:
        budgets = budgets.filter(Q(tax_title__icontains=query) |
                                 Q(tax_number__icontains=query) |
                                 Q(period__icontains=query) |
                                 Q(grup_ismi__icontains=query)).distinct()
    total_count = len(budgets)
    paginator = Paginator(budgets, 12)  # Sayfa başına nesne sayısı 12
    page = request.GET.get('page')  # Sayfa tanımlıyoruz,
    try:
        budgets = paginator.page(page)
    except PageNotAnInteger:
        budgets = paginator.page(1)
    except EmptyPage:
        budgets = paginator.page(paginator.num_pages)
    note = f'TOPLAM KAYITLAR {total_count} ADETTİR'
    if not query and len(budgets) == 0:
        note = 'GİRDİĞİNİZ MALİ VERİ BULUNMAMAKTADIR.'
    return render(request, 'budget/index.html', {'budgets': budgets, 'note': note})


def budget_base_table(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    # adres çubuğundan denemeler için önlem
    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    print('***** Temel Tablo Görünümü :', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)
    b = detayhesaplama(budget)
    if b['L01'] != b['L02']:
        messages.warning(request, 'AKTİF VE PASİF TOPLAMLAR EŞİT DEĞİLDİR !! Lütfen girdiğiniz verileri gözden geçirin')
    if b['L6'] != b['L59']:
        messages.warning(request, 'GELİR TABLOSU ve BİLANÇO dönem net karı bilgileri uyuşmamakta!!')
    sender = 'tablo'
    context = {
        'budget': budget,
        'aktifler': b['aktif_tablosu'], 'pasifler': b['pasif_tablosu'], 'gelir_tablosu': b['gelir_tablosu'],
        'aktiftoplam': b['aktiftoplam'], 'pasiftoplam': b['pasiftoplam'], 'kar_zarar': b['kar_zarar'],
        'sender': sender
    }
    return render(request, 'budget/detail.html', context)
    # return render(request, 'budget/basetable.html', context)


def budget_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    # adres çubuğundan denemeler için önlem
    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    print('***** Detay Kalem Görünümü :', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)
    b = detayhesaplama(budget)
    if b['L01'] != b['L02']:
        messages.warning(request, 'AKTİF VE PASİF TOPLAMLAR EŞİT DEĞİLDİR !! Lütfen girdiğiniz verileri gözden geçirin')
    if b['L6'] != b['L59']:
        messages.warning(request, 'GELİR TABLOSU ve BİLANÇO dönem net karı bilgileri uyuşmamakta!!')
    sender = 'detay'
    context = {
        'budget': budget, 'M': M, 'DT': b['DT'], 'L6': b['L6'], 'L02': b['L02'], 'L01': b['L01'], 'sender': sender
    }
    return render(request, 'budget/detail.html', context)


def budget_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        grubu = Group.objects.get(user=aktif_kisi)
    except ObjectDoesNotExist:
        grubu = 'Merhaba istiklal'
    budgets = aktif_kisi.budgets.all()
    girilen = budgets.count()
    # üyelik grupları için giriş sayısı kontrol
    if str(grubu) == 'freemium':
        hak = 3
        # print(f'koşul 1 -{grubu} grup kullanıcı hakkı: {hak}')
        if girilen >= hak:
            messages.error(request, f'{hak} adet mali veri kaydı hakkınız dolmuştur, üyeliğinizi yükseltin')
            return redirect('budget:index')
        elif 1 < girilen < hak:
            messages.warning(request,
                             f'{hak} adet mali veri kaydı hakkınızdan {hak - girilen} adet hakkınız kalmıştır,'
                             f' dilediğiniz zaman üyeliğinizi yükseltebilirsiniz. İyi çalışmalar.')
        else:
            messages.info(request, f'{hak} adet mali veri kaydı hakkınız bulunmaktadır, iyi çalışmalar.')

    elif str(grubu) == 'customer':
        hak = 5
        if girilen >= hak:
            messages.error(request, f'{hak} adet mali veri kaydı hakkınız dolmuştur, üyeliğinizi yükseltin')
            return redirect('budget:index')
        elif 1 < girilen < hak:
            messages.warning(request,
                             f'{hak} adet mali veri kaydı hakkınızdan {hak - girilen} adet hakkınız bulunuyor,'
                             f' dilediğiniz zaman üyeliğinizi yükseltebilirsiniz. İyi çalışmalar.')
        else:
            messages.info(request, f'{hak} adet mali veri kaydı hakkınız bulunmaktadır, iyi çalışmalar.')

    elif str(grubu) == 'customer_plus':
        hak = 6
        if girilen >= hak:
            messages.error(request, f'{hak} adet mali veri kaydı hakkınız dolmuştur, üyeliğinizi yükseltin')
            return redirect('budget:index')
        elif 1 < girilen < hak:
            messages.warning(request,
                             f'{hak} adet mali veri kaydı hakkınızdan {hak - girilen} adet hakkınız bulunuyor, '
                             f' dilediğiniz zaman üyeliğinizi yükseltebilirsiniz. İyi çalışmalar.')
        else:
            messages.info(request, f'{hak} adet mali veri kaydı hakkınız bulunmaktadır, iyi çalışmalar.')

    else:
        hak = 250

    print(f'***** Kullanıcı : {aktif_kisi.username} - Kullanıcı Grubu : {grubu} - Toplam Girdi Sayısı: {girilen}')
    print(f'***** {hak} adet giriş hakkından {hak-girilen} adet hakkı bulunuyor, ')

    form = AddBudget(request.POST or None, request.FILES or None)
    if form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        budget.save()
        messages.success(request, 'Girdiğiniz veriler kaydedilmiştir.')
        print('***** Yeni :', budget.user.username, '--', budget.tax_title)
        return HttpResponseRedirect(budget.get_basetable_url())
    title = " Yeni Mali Veri Giriş Ekranı "

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'budget/form.html', context)


def budget_update(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    form = AddBudget(request.POST or None, request.FILES or None, instance=budget)
    if form.is_valid():
        form.save()
        print('***** Düzenlendi :', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)
        messages.success(request, 'Yaptığınız düzenlemeler kaydedilmiştir.')
        return HttpResponseRedirect(budget.get_basetable_url())
    title = (str(budget.tax_title) + " / " + str(budget.period) + " dönemini düzenle")

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'budget/form.html', context)


def budget_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    if aktif_kisi != budget.user:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')

    budget = get_object_or_404(Budget, id=id)
    print('***** Siliniyor :', budget.user.username, '--', budget.tax_title, '--', budget.id,
          '-SPU?-', aktif_kisi.username)
    budget.delete()
    messages.info(request, '{} firmasına ait {} dönem mali verisi başarıyla '
                           'silinmiştir'.format(budget.tax_title, budget.period))
    return redirect('budget:index')


def budget_lists(request, vergi):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user

    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()

    unvan = 'SİZİN BÖYLE BİR FİRMANIZ YOK'
    # adres çubuğundan vergi no deneyerek girmek isteyenlere eğer firma girişi deneyen kullanıcıya ait değilse
    #  hata yerine beklenen ekranda ünvan kısmında bu yazması için (-for error handling-)

    lists = []
    for budget in budgets:
        if budget.tax_number == vergi:
            lists.append(budget)
            unvan = budget.tax_title

    query = request.GET.get('q')
    if query:
        lists = budgets.filter(Q(tax_title__icontains=query) |
                               Q(tax_number__icontains=query) |
                               Q(period__icontains=query)).distinct()
    return render(request, 'budget/lists.html', {'lists': lists, 'vergi': vergi, 'unvan': unvan})


def budget_spread(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    print('***** Spread :', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)

    b = spreadhesaplama(budget)

    context = {
        'budget': budget, 'O': Oran, 'M': M, 'S': Spread, 'AT': b['AT'], 'PT': b['PT'], 'GT': b['GT'],
        'FG': b['FG'], 'AG': b['AG'], 'KG': b['KG'], 'nis': b['nis'], 'mg1': b['mg1']
    }

    return render(request, 'budget/spread.html', context)


def budget_compare(request):
    global budget1, budget2, budget3
    if not request.user.is_authenticated:  # bu if koşulu ile kullanıcı girişi yapılmamışsa 404 sayfası gönderir
        return redirect('accounts:register')
    everything_ok = True
    liste = request.POST.getlist('checkbox')
    # print(liste)

    if len(liste) <= 1 or len(liste) > 3:
        everything_ok = False
        messages.error(request, 'En az 2 en çok 3 dönem seçmelisiniz!! Tarayıcınızdan geri yaparak önceki '
                                'sayfaya dönebilirsiniz')
        context = {'everything_ok': everything_ok}
        return render(request, 'budget/compare.html', context)

    budgets = [Budget.objects.get(id=id) for id in liste]

    def diz(budget):
        return budget.period

    budgets.sort(key=diz)
    count = 0
    for budget in budgets:
        count += 1
        if count == 1:
            budget1 = budget
        if count == 2:
            budget2 = budget
        if count == 3:
            budget3 = budget
    if count == 3:
        if not budget1.tax_number == budget2.tax_number == budget3.tax_number:
            messages.info(request, '{}  ,  {}  ve  {}   firmalarının mali verilerini '
                                      'karşılaştırıyorsunuz'.format(budget1.tax_title, budget2.tax_title,
                                                                    budget3.tax_title))
    else:
        if not budget1.tax_number == budget2.tax_number:
            messages.info(request, '{}   ile   {}   firmalarının mali verilerini '
                                      'karşılaştırıyorsunuz'.format(budget1.tax_title, budget2.tax_title))

    period1 = hesaplamalar(budget1)
    # print('1. dönem için', len(period1['a']), len(aktifler))
    period2 = hesaplamalar(budget2)
    # print('2. dönem için', period2)
    if len(liste) == 3:
        period3 = hesaplamalar(budget3)
        # print('3. dönem için', period3)
    else:
        period3 = None

    if len(liste) == 3:
        A = [(aktifler[i], period1['a'][i], period2['a'][i], period3['a'][i]) for i in range(0, len(aktifler))]
    else:
        A = [(aktifler[i], period1['a'][i], period2['a'][i]) for i in range(0, len(aktifler))]

    if len(liste) == 3:
        P = [(pasifler[i], period1['p'][i], period2['p'][i], period3['p'][i]) for i in range(0, len(pasifler))]
    else:
        P = [(pasifler[i], period1['p'][i], period2['p'][i]) for i in range(0, len(pasifler))]

    if len(liste) == 3:
        G = [(gelir[i], period1['g'][i], period2['g'][i], period3['g'][i]) for i in range(0, len(gelir))]
    else:
        G = [(gelir[i], period1['g'][i], period2['g'][i]) for i in range(0, len(gelir))]

    if len(liste) == 3:
        FG = [(finansal[i], period1['finansal_g'][i], period2['finansal_g'][i], period3['finansal_g'][i])
              for i in range(0, len(finansal))]
    else:
        FG = [(finansal[i], period1['finansal_g'][i], period2['finansal_g'][i]) for i in range(0, len(finansal))]

    if len(liste) == 3:
        KG = [(karlilik[i], period1['karlilik_g'][i], period2['karlilik_g'][i], period3['karlilik_g'][i])
              for i in range(0, len(karlilik))]
    else:
        KG = [(karlilik[i], period1['karlilik_g'][i], period2['karlilik_g'][i]) for i in range(0, len(karlilik))]

    if len(liste) == 3:
        AG = [(aktivite[i], period1['aktivite_g'][i], period2['aktivite_g'][i], period3['aktivite_g'][i])
              for i in range(0, len(aktivite))]
    else:
        AG = [(aktivite[i], period1['aktivite_g'][i], period2['aktivite_g'][i]) for i in range(0, len(aktivite))]

    if budget1.grup_ismi:
        grup = budget1.grup_ismi
    else:
        grup = None

    if len(liste) == 3:
        context = {
            'budgets': budgets, 'budget1': budget1, 'budget2': budget2, 'budget3': budget3,
            'period1': period1, 'period2': period2, 'period3': period3,
            'A': A, 'P': P, 'G': G, 'FG': FG, 'KG': KG, 'AG': AG,
            'sayi': 3, 'grup': grup, 'everything_ok': everything_ok

        }
    else:
        context = {
            'budgets': budgets, 'budget1': budget1, 'budget2': budget2,
            'period1': period1, 'period2': period2,
            'A': A, 'P': P, 'G': G, 'FG': FG, 'KG': KG, 'AG': AG,
            'sayi': 2, 'grup': grup, 'everything_ok': everything_ok
        }
    return render(request, 'budget/compare.html', context)


def budget_group_list(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user  # istek gönderen kullanıcıyı aktif kişi değişkenine atadık
    # secili = get_object_or_404(Budget, id=id)

    try:
        secili = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')

    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    # bu kullanıcının oluşturduğu budgetleri budgets listesine attık
    grup = 'SİZİN BÖYLE BİR FİRMANIZ YOK'  # adres çubuğundan vergi no deneyerek girmek isteyenlere eğer firma
    # girişi deneyen kullanıcıya ait değilse hata sayfası yerine beklenen ekranda ünvan kısmında bu yazması için

    lists = []
    liste = []
    for budget in budgets:
        if budget.grup_ismi == secili.grup_ismi:
            lists.append(budget)
            liste.append(budget.tax_title)
            grup = budget.grup_ismi
    gruplist = set(liste)

    query = request.GET.get('q')
    # query nin boş olup olmadığını test ediyor, boş ise false verecek ve if bloğuna girmeyecek. if bloğunun içinde
    # aranan şeyi Q nesnesinin yardımı ile birden fazla alanda arayarak eşleşenleri yakalıyor, distinct() metodu ise
    # Q nesnelerinin aynı nesneyi yakalamış olma ihtimaline karşı her nesneyi br kez getirip budgets listesine atıyor
    if query:
        lists = budgets.filter(Q(tax_title__icontains=query) |
                               Q(tax_number__icontains=query) |
                               Q(period__icontains=query)).distinct()

    context = {
        'secili': secili,
        'lists': lists,
        'grup': grup,
        'gruplist': gruplist
    }
    return render(request, 'budget/lists.html', context)


def budget_group_spread(request, slug):
    global grup
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('accounts:register')
    aktif_kisi = request.user
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    secim = request.POST.getlist('radio')
    print('***** (group spread) Seçim: ', secim)
    grup = None
    # yapılan seçimleri listelemek için listelerin mali veri dönemine göre sıralanmasını sağlamak için tanımlanmıştır;

    def diz(liste):
        return liste[0].period

    group_companies = []
    objectlist = []
    numberlist = []
    titlelist = []
    periodlist = []
    for budget in budgets:
        if budget.grup_ismi and slugify(budget.grup_ismi) == slug:
            group_companies.append(budget)
            objectlist.append(budget)
            numberlist.append(budget.tax_number)
            titlelist.append(budget.tax_title)
            periodlist.append(budget.period)
            grup = budget.grup_ismi
    grupset = set(titlelist)
    numberset = set(numberlist)
    periodset = set(periodlist)
    # print('VKN ler', numberset, 'Dönemler', periodset)
    ll = []
    donemler = []
    for y in periodset:
        # print(y, 'dönemi için döngü çalıştı')
        lll = []
        for a in objectlist:
            # print(a, 'nesnesi için döngü çalıştı')
            if a.tax_number in numberset and a.period == y:
                print(a.tax_title, 'için', a.period, 'eklendi....')
                lll.append(a)
                ll.append(a)
            # elif a.tax_number in numberset and a.period != y:
            #     # print(a.tax_title, 'için', y, 'bulunamadı!!!!!')
        donemler.append(lll)

    # print('eleman silme öncesi dönemler listesi = ', donemler)

    i = 0
    for d in donemler:
        print('{}. elemanın dönemi : '.format(i + 1), d[0].period)
        print('{}. elemanın içerik sayısı : '.format(i + 1), len(d))
        i += 1
        if len(d) != len(numberset):
            messages.warning(request, '{} grubu için {} dönemine ait girilmemiş veriler var!'.format(slug, d[0].period))
            donemler.remove(d)
    donemler.sort(key=diz)
    # print('objectlist listesi = ', objectlist)
    # print('lll listesi = ', lll)
    # print('ll listesi = ', ll)
    # print('eleman silme sonrası dönemler listesi = ', donemler)
    # print(request.POST.get('radio'))

    if len(secim) == 1:
        secilen = donemler[int(secim[0]) - 1]
        # print(secilen[0].period)
        secilen_donem = secilen[0].period
        if len(secilen) != len(numberset):
            secim = None
            messages.warning(request, 'Seçilen dönemde grubun bazı firmalarının mali verileri girilmemiş!!')
            print('seçilen dönemde eksik veriler var!!')
        # print(secilen)
        d = groupspread(secilen)

    # birden fazla seçim yapılmış ise şimdi seçim yapılan dönemler için karşılaştırmalı spread oluşturuyoruz.
    if len(secim) == 2:
        everything_ok = True
        secilenler = [donemler[int(x) - 1] for x in secim]
        secilenler.sort(key=diz)
        budget1 = secilenler[0][0]
        budget2 = secilenler[1][0]
        period1 = groupspread(secilenler[0])
        period2 = groupspread(secilenler[1])
        A = [(aktifler[i], period1['a'][i], period2['a'][i]) for i in range(0, len(aktifler))]
        P = [(pasifler[i], period1['p'][i], period2['p'][i]) for i in range(0, len(pasifler))]
        G = [(gelir[i], period1['g'][i], period2['g'][i]) for i in range(0, len(gelir))]
        FG = [(finansal[i], period1['finansal_g'][i], period2['finansal_g'][i]) for i in range(0, len(finansal))]
        KG = [(karlilik[i], period1['karlilik_g'][i], period2['karlilik_g'][i]) for i in range(0, len(karlilik))]
        AG = [(aktivite[i], period1['aktivite_g'][i], period2['aktivite_g'][i]) for i in range(0, len(aktivite))]
        print(budget1.period, 've', budget2.period, 'dönemleri için karşılaştırmalı grup spread oluşturuldu.')

        context = {
            'grup': grup, 'group_companies': grupset,
            'budget1': budget1, 'budget2': budget2, 'period1': period1, 'period2': period2,
            'A': A, 'P': P, 'G': G, 'FG': FG, 'KG': KG, 'AG': AG,
            'company_count': len(numberset), 'period_count': len(secim),
            'everything_ok': everything_ok
        }
        return render(request, 'budget/compare.html', context)

    elif len(secim) == 3:
        everything_ok = True
        secilenler = [donemler[int(x) - 1] for x in secim]
        secilenler.sort(key=diz)
        budget1 = secilenler[0][0]
        budget2 = secilenler[1][0]
        budget3 = secilenler[2][0]
        period1 = groupspread(secilenler[0])
        period2 = groupspread(secilenler[1])
        period3 = groupspread(secilenler[2])
        A = [(aktifler[i], period1['a'][i], period2['a'][i], period3['a'][i]) for i in range(0, len(aktifler))]
        P = [(pasifler[i], period1['p'][i], period2['p'][i], period3['p'][i]) for i in range(0, len(pasifler))]
        G = [(gelir[i], period1['g'][i], period2['g'][i], period3['g'][i]) for i in range(0, len(gelir))]
        FG = [(finansal[i], period1['finansal_g'][i], period2['finansal_g'][i], period3['finansal_g'][i])
              for i in range(0, len(finansal))]
        KG = [(karlilik[i], period1['karlilik_g'][i], period2['karlilik_g'][i], period3['karlilik_g'][i])
              for i in range(0, len(karlilik))]
        AG = [(aktivite[i], period1['aktivite_g'][i], period2['aktivite_g'][i], period3['aktivite_g'][i])
              for i in range(0, len(aktivite))]
        print(budget1.period, ' , ', budget2.period, 've', budget3.period,
              'dönemleri için karşılaştırmalı grup spread oluşturuldu.')

        context = {
            'grup': grup, 'group_companies': grupset,
            'budget1': budget1, 'budget2': budget2, 'budget3': budget3,
            'period1': period1, 'period2': period2, 'period3': period3,
            'A': A, 'P': P, 'G': G, 'FG': FG, 'KG': KG, 'AG': AG,
            'company_count': len(numberset), 'period_count': len(secim),
            'everything_ok': everything_ok
        }
        return render(request, 'budget/compare.html', context)

    elif len(secim) > 3:
        secim = None
        messages.warning(request, 'Lütfen karşılaştırmalı spread için en fazla 3 dönem seçiniz !!')

    if secim:
        secildi = True
        print(secilen[0].period, 'dönem grup spread oluşturuldu.')
        context = {
            'grup': grup, 'secildi': secildi, 'slug': slug, 'secim': secim, 'secilen_donem': secilen_donem,
            'secilen': secilen,
            'AT': d['AT'], 'PT': d['PT'], 'GT': d['GT'], 'FG': d['FG'], 'AG': d['AG'], 'KG': d['KG'],
            'nis': d['nis'], 'mg1': d['mg1'], 'O': Oran, 'sayi': len(numberset)
        }
        return render(request, 'budget/spread.html', context)
    else:
        secildi = False
        print('Doğru seçim yapılmadı ya da henüz seçim yapılmadı!!')
        context = {
            'secildi': secildi,
            'donemler': donemler,
            'companies': grupset,
            'lists': objectlist,
            'grup': grup,
            'll': ll, 'slug': slug
        }
    return render(request, 'budget/groups.html', context)


def budget_analysis(request, id):
    if not request.user.is_authenticated:  # bu if koşulu ile kullanıcı girişi yapılmamışsa 404 sayfası gönderir
        return redirect('accounts:register')

    aktif_kisi = request.user

    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')

    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    form = AddComments(request.POST or None, request.FILES or None, instance=budget)
    if form.is_valid():  # üst satırda get object ile çektiğim formu instance ile formun içine atıyorum
        form.save()
        messages.success(request, 'Eklediğiniz görüş, yorum ve öneriler kaydedilmiştir.')
        return HttpResponseRedirect(budget.get_report_url())
    title = (str(budget.tax_title) + " / " + str(budget.period) + " mali verilerine ilişkin görüş, yorum ve öneriler")
    yorumla = True
    print('***** Rapor Hazırlanıyor : ', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)
    d = hesaplamalar(budget)

    context = {
        'yorumla': yorumla,
        'title': title, 'budget': budget, 'form': form,
        'donen': d['donen_varlik'], 'duran': d['duran_varlik'],
        'kv_borc': d['kv_borc'], 'uv_borc': d['uv_borc'], 'ozkaynak': d['ozkaynak'],
        'gelir_tablosu': d['gelir_tablosu'], 'finansal_gostergeler': d['finansal_gostergeler'],
        'aktivite_gostergeleri': d['aktivite_gostergeleri'], 'karlilik_gostergeleri': d['karlilik_gostergeleri'],
        'nis': d['nis'], 'cost_income': d['mg1']
    }
    return render(request, 'budget/form.html', context)
    # print(request.POST.get('radio'))
    # return HttpResponse('Analiz sayfasıdır, henüz tasarım aşamasındadır, sabrınız için teşekkür ederiz. :)')


def budget_report(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:register')

    aktif_kisi = request.user
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')

    if budget.user != aktif_kisi and not aktif_kisi.is_superuser:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    print('***** Raporlanıyor : ', budget.user.username, '--', budget.tax_title, '-SPU?-', aktif_kisi.username)
    tarih = datetime.datetime.strftime(datetime.datetime.now(), '%d %B %Y')
    data = '{} için {} {} tarafından hazırlanan rapordur.'.format(budget.tax_title,
                                                                  budget.user.first_name, budget.user.last_name)

    b = detayhesaplama(budget)

    context = {
        'budget': budget,
        'data': data,
        'aktif_kisi': aktif_kisi,
        'tarih': tarih,
        'aktifler': b['aktif_tablosu'], 'pasifler': b['pasif_tablosu'], 'gelir_tablosu': b['gelir_tablosu'],
        'aktiftoplam': b['aktiftoplam'], 'pasiftoplam': b['pasiftoplam'], 'kar_zarar': b['kar_zarar'],
        'temel_oran': b['temel_oran'], 'finansal_oran': b['finansal_oran'], 'aktivite_oran': b['aktivite_oran'],
        'karlilik_oran': b['karlilik_oran']
    }
    return render(request, 'budget/report.html', context)


def budget_pdf(request, id):
    if not request.user.is_authenticated and not request.user.is_superuser:
        return redirect('accounts:register')
    aktif_kisi = request.user
    # request in alındığı template in url sini alıyoruz
    print('fonksiyona gelen id : ', id)
    # # print(request.META)
    # print(request.META['CONTENT_LENGTH'])
    # referer_url = request.META['HTTP_REFERER']
    # print(referer_url)
    try:
        budget = Budget.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.info(request, 'Yanlış bir giriş denediniz')
        return redirect('budget:index')
    d = hesaplamalar(budget)

    response = HttpResponse(content_type='text/csv')   # MIME Type
    response['Content-Disposition'] = 'attachment; filename= "rapor.csv"'

    writer = csv.writer(response)
    writer.writerow(['RAPOR'])
    writer.writerow([budget.tax_title, budget.period])
    writer.writerow(['Firma/Grup ve Yönetici Detay Bilgileri :', budget.company])
    writer.writerow(['Firma/Grup Mali Veri Detaylarına İlişkin Açıklamalar :', ''])
    writer.writerow(['Bilanço Aktifleri :', ''])
    writer.writerow(['DÖNEN VARLIKLAR:', budget.comment1])
    writer.writerow(['DURAN VARLIKLAR:', budget.comment2])
    writer.writerow(['Bilanço Pasifleri :', ''])
    writer.writerow(['YABANCI KAYNAKLAR:', budget.comment3])
    writer.writerow(['ÖZKAYNAKLAR:', budget.comment4])
    writer.writerow(['Gelir Tablosu:', budget.comment5])
    writer.writerow(['Oran Analizi:', budget.comment6])
    writer.writerow(['Firmanın/Grubun Mali Yapısı:', budget.comments])
    writer.writerow(['Firma/Grup İçin Tavsiyeler:', budget.advice])

    return response

