
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.contrib import messages
from django.db.models import Q
from mesaj.forms import AddMesaj
from django.db.models import Q
from mesaj.models import Mesaj
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.


def mesaj_index(request):
    if not request.user.is_superuser:
        raise Http404
    mesajlar = Mesaj.objects.all()
    context = {
        'mesajlar': mesajlar
    }
    return render(request, 'accounts/admin.html', context)


def mesaj_detail(request, id):
    if not request.user.is_authenticated:
        raise Http404
    aktif_kisi = request.user
    mesaj = get_object_or_404(Mesaj, id=id)
    if aktif_kisi.username != mesaj.name and not request.user.is_superuser:
        raise Http404

    context = {
        'aktif_kisi': aktif_kisi,
        'mesaj': mesaj
    }
    return render(request, 'mesaj/detail.html', context)


def mesaj_create(request):
    form = AddMesaj(request.POST or None, request.FILES or None)
    if form.is_valid():
        # print(f'****Form doldururldu mu?-{request.method} : {form.is_valid()}')
        mesaj = form.save(commit=False)
        if request.user.is_authenticated:
            mesaj.name = request.user.username
            mesaj.email = request.user.email
        mesaj.save()
        messages.success(request, 'Mesajınız gönderilmiştir, iletişim bilgilerinizin doğru olması halinde '
                                  'en kısa sürede tarafınıza dönüş yapılacaktır, ilginiz için teşekkür ederiz.')
        return HttpResponseRedirect(mesaj.get_create_url())
    else:
        print(f'****Form doldururldu mu?-{request.method} : {form.is_valid()}')

    mailimiz = 'destek@finestfinans.net'  # iletişim bilgilerimiz
    telefonumuz = ''  # ileişim bilgilerimiz 0532 257 30 10

    context = {
        'form': form,
        'title': 'Bize Mesaj Gönder',
        'mailimiz': mailimiz, 'telefonumuz': telefonumuz
    }
    return render(request, 'mesaj/form.html', context)


def mesaj_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    mesaj = get_object_or_404(Mesaj, id=id)   # id si gelen nesneyi alıp haber değişkenine tanımlıyorum
    form = AddMesaj(request.POST or None, request.FILES or None, instance=mesaj)
    if form.is_valid():            # üst satırda get object ile çektiğim formu instance ile formun içine atıyorum
        form.save()
        messages.success(request, 'Düzenlemeler kaydedilmiştir.')
        return HttpResponseRedirect(mesaj.get_absolute_url())
    context = {
        'form': form,
        'title': 'Mesaja Cevap Ver'
    }
    return render(request, 'mesaj/form.html', context)


def mesaj_delete(request, id):
    if not request.user.is_superuser:     # bu if koşulu ile kullanıcı girişi yapılmamışsa 404 sayfası gönderir
        raise Http404

    mesaj = get_object_or_404(Mesaj, id=id)
    mesaj.delete()
    messages.success(request, 'Mesaj başarıyla silinmiştir')
    return redirect('accounts:admin')

