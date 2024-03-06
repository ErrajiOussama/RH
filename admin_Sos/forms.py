from django.apps import apps
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.core.exceptions import ValidationError

collaborateur = apps.get_model('admin_Sos','Collaborateur')

class Collaborateurform(forms.ModelForm):
    class Meta:
        model=Collaborateur
        fields = ['Statut','Nom', 'Prenom','Sexe', 'Date_de_naissance','Situation_familiale','Nombre_d_enfants','N_CIN','N_Passeport','Nationalité','Adresse_postale','Ville','E_mail','Declaration_CNSS','N_de_téléphone','RIB','N_CNSS','Type_de_contrat','Salaire_base','Poste','CSP','Date_d_entrée','Date_de_Sortie','Activite','Motif_de_départ','Commentaire']
       
class SalaireForm(forms.ModelForm):
    class Meta:
        model=Collaborateur
        fields=['Nbre_d_heures_Travaillees','Avance_sur_salaire','Prime_Produit']      


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



class HoursWorkedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(HoursWorkedForm, self).__init__(*args, **kwargs)
        for collaborateur in Collaborateur.objects.filter(CSP='AGENT'):
            label = 'Hours worked for {} {}'.format(collaborateur.Prenom, collaborateur.Nom)
            self.fields['hours_worked_{}'.format(collaborateur.id)] = forms.DecimalField(label=label, required=False)

    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation logic here if needed
        return cleaned_data

class PrimeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrimeForm, self).__init__(*args, **kwargs)
        for collaborateur in Collaborateur.objects.filter(CSP='AGENT'):
            label = 'Prime for {} {}'.format(collaborateur.Prenom, collaborateur.Nom)
            self.fields['prime_{}'.format(collaborateur.id)] = forms.DecimalField(label=label, required=False)

    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation logic here if needed
        return cleaned_data