# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class UserLoginForm(forms.Form):
    username  = forms.CharField(max_length=250, help_text='Required.')
    password  = forms.CharField(widget=forms.PasswordInput(), max_length=250, help_text='Required')

    def __init__(self, *args, **kwargs):
            super(UserLoginForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
            self.fields['password'].widget.attrs['placeholder'] = 'Hasło'

            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
            super(UserRegisterForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
            self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
            self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
            self.fields['password2'].widget.attrs['placeholder'] = 'Powtórz hasło'

            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
