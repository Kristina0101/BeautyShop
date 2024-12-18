from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    username = forms.CharField(label='Логин', max_length=150)
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Фото', required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['image']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
