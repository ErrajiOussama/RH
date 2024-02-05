from django.db.models.fields import Field
from .models import *
from django import forms
from datetime import datetime
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class Collaborateurform(forms.ModelForm):
    
    class Meta:
        model=Collaborateur
        fields= '__all__'
        