from django import forms
from mesaj.models import Mesaj
from django.contrib import messages
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.bootstrap import StrictButton
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AddMesaj(forms.ModelForm):

    class Meta:
        model = Mesaj
        fields = [
            'name',
            'email',
            'title',
            'content',
            'files',
        ]

    def __init__(self, *args, **kwargs):
        super(AddMesaj, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-vertical'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'submit'
        self.helper.layout = Layout(
            'name',
            'email',
            'title',
            'content',
            'files',
            StrictButton('KAYDET / GÖNDER', css_class='btn-outline-info', type='submit'),
        )

    def clean(self):
        form = self.cleaned_data
        content = self.cleaned_data.get('content')
        # print(f'TİPİİİİ****{content}!!!!')
        if content == '':
            # print(f'****{content}!!!!')
            raise forms.ValidationError('Lütfen mesaj içeriğini yazınız!')
        return form
