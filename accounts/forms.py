
from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate, models
from django.contrib.auth.models import User, UserManager, Group, Permission


freemium, created = Group.objects.get_or_create(name='freemium')  # üyelik yetki grubu tanımları
customer, created = Group.objects.get_or_create(name='customer')
customer_plus, created = Group.objects.get_or_create(name='customer_plus')
customer_pro, created = Group.objects.get_or_create(name='customer_pro')
premium, created = Group.objects.get_or_create(name='premium')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Kullanıcı Adı')
    password = forms.CharField(max_length=50, label='Parola', widget=forms.PasswordInput)

    # views.py dosyasında oluşturduğumuz login_view metodunda kullandığımız authenticated metodu
    # girilen kullanıcı adı ve şifreyi geçerli bir kullanıcı ile eşleştiremediğinde hata sayfası alıyoruz
    # bunun yerine bir uyarı ekranı almak için aşağıdaki metodu tanımlıyoruz.

    def clean(self):
        kisi = self.cleaned_data.get('username')   # cleaned_data metodu geçerli ise veri aktarımı yapar yoksa boş döner
        sifre = self.cleaned_data.get('password')  # veri aktarılmış ise kisi ve sifre değişkenleri dolu gelecektir
        if kisi and sifre:                        # eğer bu datalar boş olursa false dolu olursa True döner (dolu ise)
            user = authenticate(username=kisi, password=sifre)  # sistemde kullanıcı varmı kontrol edip varsa döndürür
            if not user:  # eğer user nesnesi boş ise aşağıdaki hata mesajı gelir dolu ise bu if satırına girmez
                raise forms.ValidationError('Kullanıcı Adı veya Parola yanlış girilmiştir !')
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label='Kullanıcı Adı')
    first_name = forms.CharField(max_length=50, label='Adınız')
    last_name = forms.CharField(max_length=50, label='Soyadınız')
    email = forms.EmailField(max_length=50, label='e-posta adresiniz')
    password1 = forms.CharField(max_length=50, label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, label='Parola Doğrulama', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1',
            'password2',
        ]

    # girilen şifre1 ve şifre2 nin doğrulamasını yapalım;
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # password1, password2 alanları dolu ve birbirine eşit değil ise şeklinde bir if koşulu ekleyerek uyarı veririz
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Parolalar eşleşmiyor !')
        return password2  # Eğer bir hata yok ise password2 ye geri döndürüyoruz

    # girilen kullanıcı adının mevcut kullanıcılar ile çakışmasını önlemek için kullanıcı adı denetimi koyalım;
    def clean_username(self):
        kisi = self.cleaned_data.get('username')
        kisiler = User.objects.all()
        for user in kisiler:
            if user.username == kisi:
                raise forms.ValidationError('{} adında bir kullanıcı bulunmaktadır,'
                                            ' kullanıcı adını değiştiriniz.'.format(kisi))
        return kisi


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(max_length=50, label='Mevcut Parolanız', widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=50, label='Yeni Parolanız', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, label='Yeni Parola Onayınız', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'old_password',
            'password1',
            'password2',
        ]

    # girilen şifre1 ve şifre2 nin doğrulamasını yapalım;
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        # password1, password2 alanları dolu ve birbirine eşit değil ise şeklinde bir if koşulu ekleyerek uyarı veririz
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Yeni parolalarınız eşleşmiyor !')
        return password2  # Eğer bir hata yok ise password2 ye geri döndürüyoruz

    # def clean_old_password(self):
    #     sifre = self.cleaned_data.get('old_password')
    #     kisi = self.instance
    #     print('forms çalıştı', type(kisi), 'türünde', kisi, 'şifresi', sifre)
    #     if kisi and sifre:
    #         user = authenticate(user=kisi, password=sifre)
    #         print('forms daki if çalıştı', user, 'türü', type(user))
    #         if not user:
    #             raise forms.ValidationError('Mevcut parolanızı doğru girmediniz!!')
    #     return sifre


class PasswordResetForm(forms.ModelForm):
    email = forms.EmailField(max_length=50, label='e-posta adresiniz')

    class Meta:
        model = User
        fields = [
            'email',
        ]

    def clean_email(self):
        posta = self.cleaned_data.get('email')
        kisiler = User.objects.all()
        conflict = []
        for kisi in kisiler:
            if kisi.email == posta:
                conflict.append(kisi)
        if len(conflict) == 0:
            raise forms.ValidationError('Girdiğiniz e-posta adresi sistemde kayıtlı değildir. '
                                            'Lütfen Üyelik bilgilerinizdeki e-posta adresini giriniz')
        if len(conflict) > 1:
            raise forms.ValidationError('E-posta adresi birden fazla kullanıcıda kayıtlıdır!!')

        return posta


class InfoUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='Adınız')
    last_name = forms.CharField(max_length=50, label='Soyadınız')
    email = forms.EmailField(max_length=50, label='e-posta adresiniz')

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
        ]

