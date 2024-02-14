from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    Salaire_Avancee = models.FloatField(null=True,blank=True)
    salaire_finale = models.IntegerField(null=True,blank=True)
    anciennetee = models.IntegerField(null=True, blank=True)
    user =models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)

    def calculate_work_duration_in_months(self):
        if self.Date_d_entrée and self.Date_de_Sortie:
            start_date = self.Date_d_entrée
            end_date = self.Date_de_Sortie

            years = end_date.year - start_date.year
            months = end_date.month - start_date.month

            # Calculate total months worked
            total_months_worked = years * 12 + months

            # Adjust for cases where the end date day is before the start date day
            if end_date.day < start_date.day:
                total_months_worked -= 1

            return total_months_worked
        else:
            return None  # Or handle the case where one of the dates is missing


    def save(self, *args, **kwargs):
        
        work_duration_in_months = self.calculate_work_duration_in_months()

        # Save work duration in months to the field
        if work_duration_in_months is not None:
            self.work_duration_in_months = work_duration_in_months

        if self.Date_de_naissance:
            today = date.today()
            age = today.year - self.Date_de_naissance.year - ((today.month, today.day) < (self.Date_de_naissance.month, self.Date_de_naissance.day))
            self.Age = age
            
        super().save(*args, **kwargs)
    
    def __str__(self): 
        return str(self.Nom)
    
    