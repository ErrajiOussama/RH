from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Collaborateur(models.Model):
    STATUT_statut = (
        ('ACTIF','ACTIF'),
        ('INACTIF','INACTIF'),
        ('FORMATION','FORMATION'),
        ('STAGE','STAGE'),
    )

    STATUT_causededepart = (
        ('Demission','Demission'),
        ('Licenciement','Licenciement'),
        ('FPE','FPE'),
        ('Fin de contrat','Fin de contrat'),
        ('Comportement','Comportement'),
        ('Etudes','Etudes'),
        ('Sans motif(Volantaire)','Sans motif(Volantaire)'),
    )
    Contart = (
        ('Etrange','Etrange'),
        ('Stage','Stage'),
        ('CDD','CDD'),
        ('CDI','CDI'),
    )

    statut_sexe = (
        ('H','H'),
        ('F','F'),
    )

    statut_Poste = (
        ('Agent','Agent'),
        ('Admin','Admin'),
        ('RH','RH'),
    )



    Statut = models.CharField(max_length=10,null=True,blank=True,choices=STATUT_statut)
    Nom = models.CharField(max_length=50,null=True,blank=True)
    Prenom = models.CharField(max_length=50,null=True,blank=True)
    Sexe = models.CharField(max_length=5,null=True,blank=True,choices=statut_sexe)
    Date_de_naissance = models.DateField(null=True,blank=True)
    Age = models.PositiveIntegerField(null=True,blank=True)
    Situation_familiale = models.CharField(max_length=10, null=True,blank=True)
    Nombre_d_enfants = models.FloatField( null=True,blank=True)
    N_CIN =models.CharField(max_length=12 ,null=True,blank=True)
    N_Passeport=models.CharField(max_length=30 ,null=True,blank=True)
    Nationalité=models.CharField(max_length=20,null=True,blank=True)
    Adresse_postale=models.CharField(max_length=200,null=True,blank=True)
    Ville=models.CharField(max_length=20,null=True,blank=True)
    E_mail= models.EmailField(null=True,blank=True)
    N_de_téléphone=models.CharField(max_length=20,null=True,blank=True)
    RIB = models.CharField(max_length=30,null=True,blank=True)
    N_CNSS= models.CharField(max_length=20,null=True,blank=True)
    Type_de_contrat= models.CharField(max_length=10,null=True,blank=True,choices=Contart)
    Salaire_base = models.PositiveBigIntegerField(null=True,blank=True)
    Prime = models.FloatField(default=0,null=True,blank=True)
    Poste = models.CharField(max_length=10,null=True,blank=True,choices=statut_Poste)
    Date_d_entrée = models.DateField(null=True,blank=True)
    Date_de_Sortie = models.DateField(null=True,blank=True)
    Taux_Horaire= models.FloatField(default=0,null=True,blank=True)
    Salaire_Avancee = models.FloatField(default=0,null=True,blank=True)
    salaire_finale = models.IntegerField(null=True,blank=True)
    anciennetee = models.IntegerField(null=True, blank=True)
    S_H = models.FloatField(null=True, blank=True)
    Commentaire = models.CharField(max_length=1000,null=True,blank=True)
    Motif_de_départ = models.CharField(max_length=1000,null=True,blank=True,choices=STATUT_causededepart)
    user =models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)

    def calculate_work_duration_in_months(self):
        today = date.today()

        if self.Date_d_entrée:
            start_date = self.Date_d_entrée
            if self.Date_de_Sortie:
                end_date = self.Date_de_Sortie
            else:
                end_date = today  # Use current date if Date_de_Sortie is not provided

            years = end_date.year - start_date.year
            months = end_date.month - start_date.month

            # Calculate total months worked
            total_months_worked = years * 12 + months

            # Adjust for cases where the end date day is before the start date day
            if end_date.day < start_date.day:
                total_months_worked -= 1

            return total_months_worked
        else:
            return None  # Or handle the case where the entry date is missing

    def save(self, *args, **kwargs):
        
        work_duration_in_months = self.calculate_work_duration_in_months()

        # Save work duration in months to the field
        if work_duration_in_months is not None:
            self.anciennetee = work_duration_in_months

        if self.Date_de_naissance:
            today = date.today()
            age = today.year - self.Date_de_naissance.year - ((today.month, today.day) < (self.Date_de_naissance.month, self.Date_de_naissance.day))
            self.Age = age

        super().save(*args, **kwargs)
    
    def __str__(self): 
        return str(self.Nom)
    
    