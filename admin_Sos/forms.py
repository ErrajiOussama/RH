from django.apps import apps
from django.forms import ModelForm
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class Collaborateurform(forms.ModelForm):
    class Meta:
        model=Collaborateur
        fields= '__all__'
        widgets = {
            'Date_de_naissance': forms.DateInput(attrs={'class': 'datepicker'}),
            'Date_d_entrée': forms.DateInput(attrs={'class': 'datepicker'}),
            'Date_de_Sortie': forms.DateInput(attrs={'class': 'datepicker'}),
            'Statut': forms.TextInput(attrs={'class': 'form-control'}),
            'Nom': forms.TextInput(attrs={'class': 'form-control'}),
            'Prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'Sexe': forms.TextInput(attrs={'class': 'form-control'}),
            'Situation_familiale': forms.TextInput(attrs={'class': 'form-control'}),
            'Nombre_d_enfants': forms.NumberInput(attrs={'class': 'form-control'}),
            'N_CIN': forms.TextInput(attrs={'class': 'form-control'}),
            'N_Passeport': forms.TextInput(attrs={'class': 'form-control'}),
            'Nationalité': forms.TextInput(attrs={'class': 'form-control'}),
            'Adresse_postale': forms.TextInput(attrs={'class': 'form-control'}),
            'Ville': forms.TextInput(attrs={'class': 'form-control'}),
            'E_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'N_de_téléphone': forms.TextInput(attrs={'class': 'form-control'}),
            'RIB': forms.TextInput(attrs={'class': 'form-control'}),
            'N_CNSS': forms.TextInput(attrs={'class': 'form-control'}),
            'Type_de_contrat': forms.TextInput(attrs={'class': 'form-control'}),
            'Salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'Prime': forms.NumberInput(attrs={'class': 'form-control'}),
            'Poste': forms.TextInput(attrs={'class': 'form-control'}),
            'Taux_Horaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'Prime_Avancee': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'stop_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        
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