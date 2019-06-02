from django.forms import CharField, PasswordInput
from django import forms

class LoginForm(forms.Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())
