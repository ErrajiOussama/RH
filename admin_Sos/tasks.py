from celery import shared_task
from django.db.models import Sum
from datetime import datetime
from .models import RH, Collaborateur

@shared_task
def calculate_payroll_and_update_rh():
    # Get the current date
    current_date = datetime.now()

    # Check if it's the beginning of the month
    if current_date.day == 1:
        # Calculate total payroll for all active collaborators
        total_payroll = Collaborateur.objects.filter(Statut='ACTIF').aggregate(total=Sum('Salaire_base'))

        # Update RH model with the total payroll and other relevant data
        rh_record = RH.objects.create(
            collaborateur_Turnover=calculate_collaborateur_turnover(),
            masse_salarial=total_payroll['total'],
            date_rh=current_date
        )
        rh_record.save()

def calculate_collaborateur_turnover():
    # Calculate collaborateur turnover percentage
    total_inactive_collaborateurs = Collaborateur.objects.filter(Statut='INACTIF').count()
    total_collaborateurs = Collaborateur.objects.count()
    if total_collaborateurs > 0:
        return round((total_inactive_collaborateurs / total_collaborateurs) * 100, 2)
    else:
        return 0