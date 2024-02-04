from django.db.models.fields import Field
from .models import *
from django import forms

class Collaborateurform(forms.ModelForm):
    class Meta:
        model=Collaborateur
        fields= '__all__'
        