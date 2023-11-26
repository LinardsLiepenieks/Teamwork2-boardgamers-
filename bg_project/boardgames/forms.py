from django import forms
from .models import Boardgame
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BoardgameForm(forms.ModelForm):
    class Meta:
        model = Boardgame
        fields = ['name', 'description', 'year_published']

    name = forms.CharField(label='Boardgame Name', max_length=255)
    description = forms.CharField(label='Description')
    year_published = forms.IntegerField(label='Year Published')


class BorrowingForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
