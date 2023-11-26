from django import forms
from .models import Boardgame
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BoardgameForm(forms.ModelForm):
    class Meta:
        model = Boardgame
        fields = ['name', 'creator', 'year_published']

    name = forms.CharField(label='Boardgame Name', max_length=255)
    creator = forms.JSONField(label='Creator')
    year_published = forms.IntegerField(label='Year Published')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BorrowingForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
