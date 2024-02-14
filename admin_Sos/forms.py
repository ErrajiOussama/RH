from django.apps import apps
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class Collaborateurform(forms.ModelForm):
    class Meta:
        model=Collaborateur
        fields= '__all__'
       
        
collaborateur = apps.get_model('admin_Sos','Collaborateur')

class registerForm(UserCreationForm):
    id = forms.IntegerField(label='Collaborator ID', required=False)    

 
    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username exists")
        return self.cleaned_data
    #group = forms.ModelChoiceField(queryset=Group.objects.get(name="Client"), required=False)
 
    class Meta:
        model = User
        fields = ['username','password1','password2','id']