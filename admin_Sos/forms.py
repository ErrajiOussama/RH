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
    Nom = forms.IntegerField(label='Nom', required=False)    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username exists")
        return self.cleaned_data
    #group = forms.ModelChoiceField(queryset=Group.objects.get(name="Client"), required=False)
 
    class Meta:
        model = User
        fields = ['username','password1','password2','id']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'