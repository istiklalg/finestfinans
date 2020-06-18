
from django import forms
from haber.models import Haber
from django.contrib import messages
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.bootstrap import StrictButton


class AddHaber(forms.ModelForm):

    class Meta:
        model = Haber
        fields = [
            'konum',
            'position',
            'button',
            'title',
            'subtitle',
            'content',
            'images',
            'link',
        ]

    def __init__(self, *args, **kwargs):
        super(AddHaber, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-vertical'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'submit'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-12'
        self.helper.layout = Layout(
            'konum',
            'position',
            'button',
            'title',
            'subtitle',
            'content',
            'images',
            'link',
            StrictButton('KAYDET', css_class='btn-outline-info', type='submit'),
        )

    def clean(self):
        form = self.cleaned_data
        subtitle = self.cleaned_data.get('subtitle')
        content = self.cleaned_data.get('content')
        position = self.cleaned_data.get('position')
        button = self.cleaned_data.get('button')
        # print(f'TİPİİİİ****{content}!!!!')
        if subtitle == '':
            raise forms.ValidationError('Lütfen haber için altbaşlık yazınız!')
        elif content == '':
            raise forms.ValidationError('Lütfen heber için içerik yazınız!')
        elif position == '' or position is None:
            raise forms.ValidationError('Lütfen anasayfa pozisyonu için yerleşim sırasını ekleyin!')
        elif button == '' or button is None:
            raise forms.ValidationError('Lütfen buton üzerinde görünecek yazıyı ekleyin!')

        return form


class TaksitliForm(forms.Form):
    tip = forms.CharField(label='Seçilen Kredi Türü : ', required=True, disabled=False)
    tutar = forms.DecimalField(label='Kredi Tutarını Girin :', decimal_places=2, max_digits=15)
    faiz = forms.DecimalField(label='Faiz Oranı Girin :', decimal_places=4, max_value=45)
    vade = forms.IntegerField(label='Kredi Vadesini Girin :', max_value=720)
    fields = [
        'tip',
        'tutar',
        'faiz',
        'vade',
    ]

    def __init__(self, *args, **kwargs):
        super(TaksitliForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-TaksitliForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'submit'
        self.helper.label_class = 'col-lg-7'
        self.helper.field_class = 'col-lg-5'
        self.helper.layout = Layout(
            'tip',
            'tutar',
            'faiz',
            'vade',
            StrictButton('HESAPLA', css_class='btn-sm btn-outline-info', type='submit'),
        )


class IskontoForm(forms.Form):
    pass



