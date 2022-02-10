from django import forms
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    username.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                                  'placeholder': 'логин', })
    password = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                                  'placeholder': 'пароль', })
    remember_me = forms.BooleanField(label='запомнить меня', required=False)
    remember_me.widget.attrs.update({'class': 'singup-check'})

    # переопределяем названия
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''

    # проверяем введенные данные
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Пользователь {username} не найден.")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Неверный пароль")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    username.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                                  'placeholder': 'логин*', })
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                                          'placeholder': 'подтвердите пароль*', })
    password = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                                  'placeholder': 'введите пароль*', })
    email = forms.EmailField(required=True)
    email.widget.attrs.update({'class': 'signin-email', 'required': 'required',
                               'placeholder': 'электронная почта*', })
    first_name = forms.CharField(required=False)
    first_name.widget.attrs.update({'class': 'signin-email', 'placeholder': 'имя', })
    last_name = forms.CharField(required=False)
    last_name.widget.attrs.update({'class': 'signin-email', 'placeholder': 'фамилия', })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['confirm_password'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''

    # валидация по определенному полю
    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        # проверка домена почты
        if domain in ['net']:
            raise forms.ValidationError(f"Регистрация для домена '{domain}' невозможна")
        # проверка наличия в базе
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Данный почтовый адрес уже зарегистрирован в системе')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'имя {username} занято')
        return username

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'signin-email'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'signin-email'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'signin-email'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'signin-email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']







