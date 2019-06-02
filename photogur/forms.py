from django.forms import CharField, PasswordInput
from django import forms
from django.forms import ModelForm
from photogur.models import Picture

class LoginForm(forms.Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class PictureForm(ModelForm):
    class Meta:
        model = Picture 
        fields = ['title', 'artist', 'url']