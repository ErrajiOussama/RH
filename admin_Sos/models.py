from django.db import models
from django.contrib.auth.models import User

class Collaborateur(models.Model):
    Statut = models.CharField(max_length=10,null=True,blank=True)
    Nom = models.CharField(max_length=10,null=True,blank=True)
    Prenom = models.CharField(max_length=10,null=True,blank=True)
    Sexe = models.CharField(max_length=5,null=True,blank=True)
    Date_de_naissance = models.DateField(null=True,blank=True)
    Age = models.PositiveIntegerField(null=True,blank=True)
    Situation_familiale = models.CharField(max_length=10, null=True,blank=True)
    Nombre_d_enfants = models.FloatField( null=True,blank=True)
    N_CIN =models.CharField(max_length=12 ,null=True,blank=True)
    N_Passeport=models.CharField(max_length=30 ,null=True,blank=True)
    Nationalité=models.CharField(max_length=20,null=True,blank=True)
    Adresse_postale=models.CharField(max_length=50,null=True,blank=True)
    Ville=models.CharField(max_length=20,null=True,blank=True)
    E_mail= models.EmailField(null=True,blank=True)
    N_de_téléphone=models.CharField(max_length=20,null=True,blank=True)
    RIB = models.CharField(max_length=30,null=True,blank=True)
    N_CNSS= models.CharField(max_length=20,null=True,blank=True)
    Type_de_contrat= models.CharField(max_length=10,null=True,blank=True)
    Salaire_base = models.PositiveBigIntegerField(null=True,blank=True)
    Prime = models.FloatField( null=True,blank=True)
    Poste = models.CharField(max_length=10,null=True,blank=True)
    Date_d_entrée = models.DateField(null=True,blank=True)
    Date_de_Sortie = models.DateField(null=True,blank=True)
    Taux_Horaire= models.FloatField(null=True,blank=True)
    Prime_Avancee = models.FloatField(null=True,blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    stop_time = models.DateTimeField(null=True,blank=True)
    elapsed_time = models.DurationField(null=True,blank=True)
    user =models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)


    def __str__(self): 
        return str(self.Nom)