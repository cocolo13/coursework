from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input', "placeholder": "логин"}
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input', "placeholder": "пароль"}
    ))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'input', "placeholder": "повтор пароля"}
    ))
    last_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(
        attrs={'class': 'input', "placeholder": "имя"}
    ))

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input', "placeholder": "Логин"}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input', "placeholder": "Пароль"}
    ))