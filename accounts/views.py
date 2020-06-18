
from django.shortcuts import render, redirect, get_object_or_404, Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, models
from django.db.models import Q
from accounts.forms import *
from budget.models import *
from haber.models import *
from mesaj.models import *
import pip


# authenticate metodu içine aldığı kullanıcı adı ve şifre yi kontrol ederek kayıtlı ise geriye bir kullanıcı
# nesnesi döndürür ve bu nesneyi user isimli değişkene atıyoruz
# Create your views here.


def login_view(request):
    form = LoginForm(request.POST or None)  # LoginForm nesnesinden gelen veriyi form değişkenine attık
    if form.is_valid():
        # cleaned_data metodu is_valid metodu True ise çalışır verilerin doğruluğunu teyit ederek almamızı sağlar
        kisi = form.cleaned_data.get('username')
        sifre = form.cleaned_data.get('password')
        user = authenticate(username=kisi, password=sifre)  # kullanıcı adı ve şifenin doğrulanması adımı
        login(request, user)  # doğrulanmış olan kullanıcıyı sisteme dahil etmek için login metodunu kullanıyoruz
        print('**** Yeniden Hoşgeldin :', kisi)
        # messages.info(request, 'Hoşgeldiniz {}'.format(user.get_full_name))
        return redirect('home')  # giriş yapan kullanıcıyı redirect metodu ile anasayfaya yönlendiriyoruz

    return render(request, 'accounts/form.html', {'form': form, 'title': 'Giriş Yapın'})
    # accounts uygulaması için urls.py oluşturmalıyız


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        kisi = form.save(commit=False)
        sifre = form.cleaned_data.get('password1')
        kisi.set_password(sifre)
        kisi.is_staff = True  # django admin panelini kullanabilmesi için stuff kullanıcı olarak tanımlıyoruz
        kisi.save()
        kisi.groups.add(freemium)
        yeni_kisi = authenticate(username=kisi.username, password=sifre)
        login(request, yeni_kisi)
        print('**** Hoşgeldin :', kisi.username)
        # messages.info(request, 'Hoşgeldiniz {}'.format(yeni_kisi.get_full_name))
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Üye Olun'})


def logout_view(request):
    print('**** Görüşmek Üzere :', request.user.username)
    logout(request)
    # messages.info(request, 'Görüşmek üzere :)')
    return redirect('home')  # çıkış işlemini logout metodu ile yaptık ve anasayfaya yönlendirdik,
                             # şimdi url sini oluşturalım ve baslik.html de bunun butonunu tanımlayalım


def password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    aktif_kisi = request.user
    kisi = aktif_kisi.username
    form = PasswordChangeForm(request.POST or None)  # PasswordChangeForm nesnesinden gelen veriyi form değişkenine attık
    if form.is_valid():
        # cleaned_data metodu is_valid metodu True ise çalışır verilerin doğruluğunu teyit ederek almamızı sağlar
        old = form.cleaned_data.get('old_password')
        if not authenticate(username=kisi, password=old):
            messages.error(request, 'Mevcut parolanızı doğru girmediniz!!')
            return redirect('accounts:change')
        sifre = form.cleaned_data.get('password1')
        aktif_kisi.set_password(sifre)
        aktif_kisi.save()
        user = authenticate(username=kisi, password=sifre)  # kullanıcı adı ve şifenin doğrulanması adımı
        login(request, user)  # doğrulanmış olan kullanıcıyı sisteme dahil etmek için login metodunu kullanıyoruz
        messages.success(request, 'Şifre değişikliğiniz başarıyla yapılmıştır.')
        return redirect('accounts:admin')  # giriş yapan kullanıcıyı redirect metodu ile admine yönlendiriyoruz

    context = {'form': form, 'aktif_kisi': aktif_kisi, 'title': 'Şifre Değiştirin'}

    return render(request, 'accounts/form.html', context)


def password_reset_view(request):
    form = PasswordResetForm(request.POST or None)  # PasswordResetForm nesnesinden gelen veriyi form değişkenine attık
    if form.is_valid():
        # cleaned_data metodu is_valid metodu True ise çalışır verilerin doğruluğunu teyit ederek almamızı sağlar
        eposta = form.cleaned_data.get('email')
        kisiler = User.objects.all()
        for kisi in kisiler:
            if kisi.email == eposta:
                if kisi.is_superuser:
                    messages.error(request, 'Yanlış bir giriş denediniz')
                    return redirect('accounts:login')
                kisi.set_password(kisi.username)
                kisi.save()
        messages.success(request, 'Şifre sıfırlama işlemine ilişkin mail gonderilmiştir,'
                                  'lütfen mailinizi kontrol ediniz.')
        return redirect('accounts:login')

    context = {
        'form': form, 'title': 'Şifrenizi sıfırlayın!',
        'exp': 'Lütfen sistemde kayıtlı e-posta adresinizi girin, mail adresinize sıfırlama bilgileri gönderilecektir.'
        }

    return render(request, 'accounts/form.html', context)


def info_update_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:register')
    # aktif kullanıcıyı alıp aktif_kisi değişkenine atıyorum, sonra InfoUpdateForm örneği alıp
    # instance ile formun aktif kişinin bilgilerini atıyorum
    aktif_kisi = request.user
    form = InfoUpdateForm(request.POST or None, instance=aktif_kisi)
    if form.is_valid():
        form.save()
        messages.success(request, 'Yaptığınız değişiklikler kaydedilmiştir.')
        return redirect('accounts:admin')
    context = {
        'form': form, 'title': 'Bilgileri Güncelleyin',
        'exp': 'Bu adımda kullanıcı adı ve şifre değişikliği yapılmamaktadır.'
    }
    return render(request, 'accounts/form.html', context)


def admin_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    aktif_kisi = request.user
    if aktif_kisi.is_superuser:
        budgets = Budget.objects.all()
    else:
        budgets = aktif_kisi.budgets.all()
    query = request.GET.get('q')
    haber_adet = 0
    kisi_adet = 0
    mesaj_adet = 0
    grup_adet = 0
    budget_adet = budgets.count()
    if aktif_kisi.is_superuser:
        gruplar = Group.objects.all()
        haberler = Haber.objects.all()
        kisiler = User.objects.all()
        kisi_grup = [(kisi, Group.objects.get(user=kisi)) for kisi in kisiler if not kisi.is_superuser]
        # print(kisi_grup)
        mesajlar = Mesaj.objects.all()
        grup_adet = gruplar.count()
        haber_adet = haberler.count()
        # kisi_adet = kisiler.count()
        kisi_adet = len(kisi_grup)
        mesaj_adet = mesajlar.count()
        # Yönetici panelinde arama çubuğunu çalışır hale getir;
        if query:
            haberler = haberler.filter(Q(title__icontains=query) |
                                       Q(subtitle__icontains=query) |
                                       Q(content__icontains=query)).distinct()
            kisiler = kisiler.filter(Q(username__icontains=query) |
                                     Q(first_name__icontains=query) |
                                     Q(last_name__icontains=query) |
                                     Q(email__icontains=query)).distinct()
            mesajlar = mesajlar.filter(Q(title__icontains=query) |
                                       Q(name__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(date__icontains=query) |
                                       Q(email__icontains=query)).distinct()
            gruplar = gruplar.filter(Q(name__icontains=query)).distinct()

    else:
        gruplar = []
        kisi_grup = []
        haberler = []
        kisiler = []
        mesajlar = [mesaj for mesaj in Mesaj.objects.all() if mesaj.email == aktif_kisi.email]
        try:
            mesaj_adet = len(mesajlar)
        except TypeError:
            print('***** Panel :', aktif_kisi.username, '-- mesajınız yok ', mesaj_adet)
            mesaj_adet = 0
    # Kullanıcının yönetim panelinde arama çubuğunu çalışır hale getir;
    if query:
        budgets = budgets.filter(Q(tax_title__icontains=query) |
                                 Q(tax_number__icontains=query) |
                                 Q(period__icontains=query) |
                                 Q(grup_ismi__icontains=query)).distinct()


    context = {
        'aktif_kisi': aktif_kisi,
        'budgets': budgets, 'budget_adet': budget_adet,
        'haberler': haberler,  'haber_adet': haber_adet,
        'kisiler': kisiler, 'kisi_adet': kisi_adet,
        'mesajlar': mesajlar, 'mesaj_adet': mesaj_adet,
        'gruplar': gruplar, 'grup_adet': grup_adet, 'kisi_grup': kisi_grup
    }
    return render(request, 'accounts/admin.html', context)



