from django.db.models.fields import Field
from .models import *
from django import forms
from datetime import datetime
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm


class Collaborateurform(forms.ModelForm):
    
    class Meta:
        model=Collaborateur
        fields= '__all__'
        widgets = {
            'Date_de_naissance': forms.DateInput(attrs={'class': 'datepicker'}),
            'Date_d_entrée': forms.DateInput(attrs={'class': 'datepicker'}),
            'Date_de_Sortie': forms.DateInput(attrs={'class': 'datepicker'}),
            # Add other fields with their respective attributes here
            'Statut': forms.TextInput(attrs={'class': 'form-control'}),
            'Nom': forms.TextInput(attrs={'class': 'form-control'}),
            'Prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'Sexe': forms.TextInput(attrs={'class': 'form-control'}),
            'Age': forms.NumberInput(attrs={'class': 'form-control'}),
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



        