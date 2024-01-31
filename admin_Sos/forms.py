"""
from django.apps import apps
from django.forms import ModelForm
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *
from django import forms
from random import choice
from string import digits
from django.core.exceptions import ValidationError
 
product = apps.get_model('Client','Client')
 
class registerForm(UserCreationForm):
 username = None
 def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'placeholder': ('Votre nom d\'utilisateur...')})
    self.fields['email'].widget.attrs.update({'placeholder': ('Votre email...')})
    self.fields['password1'].widget.attrs.update({'placeholder': ('Votre mot de passe...')})
    self.fields['password2'].widget.attrs.update({'placeholder': ('Repeter votre mot de passe...')})
 
 def clean(self):
    username = self.cleaned_data.get('username')
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email exists")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username exists")
    return self.cleaned_data
 #group = forms.ModelChoiceField(queryset=Group.objects.get(name="Client"), required=False)
 email = forms.EmailField()
 
 class Meta:
     model = User
     fields = ['username','email', 'password1', 'password2']
"""