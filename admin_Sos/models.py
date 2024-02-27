from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Collaborateur(models.Model):
    
    Statut_P= (
        ('AGENT','AGENT'),
        ('CADRE','CADRE'),
        ('TECHNICIEN','TECHNICIEN'),
        ('STAGIAIRE','STAGIAIRE'),
    )
    STATUT_statut = (
        ('ACTIF','ACTIF'),
        ('INACTIF','INACTIF'),
        ('FORMATION','FORMATION'),
        ('STAGE','STAGE'),
    )
    STATUT_activite = (
        ('FRANCE','FRANCE'),
        ('CANADA','CANADA'),
    )
    STATUT_causededepart = (
        ('Demission','Demission'),
        ('Licenciement','Licenciement'),
        ('FPE','FPE'),
        ('Fin de contrat','Fin de contrat'),
        ('Comportement','Comportement'),
        ('Etudes','Etudes'),
        ('Sans motif(Volantaire)','Sans motif(Volantaire)'),
        ('Autre','Autre'),
    )
    Contart = (
        ('Etranger','Etranger'),
        ('Stage','Stage'),
        ('CDD','CDD'),
        ('CDI','CDI'),
    )
    TTGD = (
        ('Célibataire ','Célibataire'),
        ('Marié(e)','Marié(e)'),
        ('Divorcé(e)','Divorcé(e)'),
        ('Veuf(ve)','Veuf(ve)'),
    )

    statut_sexe = (
        ('H','H'),
        ('F','F'),
    )

    statut_TF = (
        ('OUI','OUI'),
        ('NON','NON'),
    )



    Statut = models.CharField(max_length=10,null=True,blank=True,choices=STATUT_statut)
    Nom = models.CharField(max_length=500,null=True,blank=True)
    Prenom = models.CharField(max_length=500,null=True,blank=True)
    Sexe = models.CharField(max_length=50,null=True,blank=True,choices=statut_sexe)
    Date_de_naissance = models.DateField(null=True,blank=True)
    Age = models.PositiveIntegerField(null=True,blank=True)
    Situation_familiale = models.CharField(max_length=100, null=True,blank=True,choices=TTGD)
    Nombre_d_enfants = models.FloatField(default=0, null=True,blank=True)
    N_CIN =models.CharField(default="-",max_length=120 ,null=True,blank=True)
    N_Passeport=models.CharField(default="-",max_length=300 ,null=True,blank=True)
    Nationalité=models.CharField(default="-",max_length=200,null=True,blank=True)
    Adresse_postale=models.CharField(default="-",max_length=200,null=True,blank=True)
    Ville=models.CharField(default="-",max_length=100,null=True,blank=True)
    E_mail= models.EmailField(null=True,blank=True)
    Declaration_CNSS= models.CharField(max_length=100,null=True,blank=True,choices=statut_TF)
    N_de_téléphone=models.CharField(max_length=200,null=True,blank=True)
    RIB = models.CharField(default="-",max_length=300,null=True,blank=True)
    N_CNSS= models.CharField(default="-",max_length=200,null=True,blank=True)
    Type_de_contrat= models.CharField(max_length=100,null=True,blank=True,choices=Contart)
    Salaire_base = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    Nombre_de_Jour_Travaille_Admin= models.PositiveIntegerField(default=0,null=True,blank=True)
    Poste = models.CharField(max_length=100,null=True,blank=True)
    CSP = models.CharField(max_length=100,null=True,blank=True,choices=Statut_P)
    Date_d_entrée = models.DateField(null=True,blank=True)
    Date_de_Sortie = models.DateField(null=True,blank=True)
    anciennetee = models.IntegerField(default=0,null=True, blank=True)
    Motif_de_départ = models.CharField(default="-",max_length=1000,null=True,blank=True,choices=STATUT_causededepart)
    Commentaire = models.CharField(default="-",max_length=1000,null=True,blank=True)
    Prime_Produit = models.FloatField(default=0,null=True,blank=True)
    Taux_Horaire= models.FloatField(default=0,null=True,blank=True)
    Planifier= models.FloatField(default=0,null=True,blank=True)
    Avance_sur_salaire = models.FloatField(default=0,null=True,blank=True)
    S_H = models.FloatField(default=0,null=True, blank=True)
    Activite=models.CharField(max_length=100,null=True,blank=True,choices=STATUT_activite)
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
    
class MonthYearField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7  # Maximum length for 'Month Year' string
        super().__init__(*args, **kwargs)

class Salaire(models.Model):
    id_Collaborateur=models.ForeignKey(Collaborateur,on_delete=models.CASCADE)
    Date_de_salaire = MonthYearField(null=True, blank=True)
    salaire_finale = models.IntegerField(default=0,null=True,blank=True)

class Salaire_admin(models.Model):
    id_Collaborateur=models.ForeignKey(Collaborateur,on_delete=models.CASCADE)
    Date_de_salaire = MonthYearField(null=True, blank=True)
    salaire_finale = models.IntegerField(default=0,null=True,blank=True)