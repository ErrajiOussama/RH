from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from datetime import datetime, timezone
from .decorators import *
from datetime import datetime
from django.db.models import Q
from django.utils.translation import activate
from django.template.loader import get_template
from .filter import * 
from django.shortcuts import get_object_or_404
import jinja2
import pdfkit
import csv
import pandas as pd
from django.shortcuts import render
from django.contrib import messages

@login_required(login_url='login')
def IndexView(request):
    current_date = datetime.now().date()
    events = Event.objects.filter(Date_debut__lte=current_date, Date_fin__gte=current_date)
    print(events.count())

    # Separate events based on priority
    events_eleve = []
    events_moyen = []
    events_faible = []

    for event in events:
        if event.priorite == "ELEVE":
            events_eleve.append(event)
        elif event.priorite == "MOYENE":
            events_moyen.append(event)
        elif event.priorite == "FAIBLE":
            events_faible.append(event)

    events_selected = []
    events_selected.extend(events_eleve[:4])
    events_selected.extend(events_moyen[:4 - len(events_selected)])
    events_selected.extend(events_faible[:4 - len(events_selected)])

    context = {
        'events': events_selected,
    }
    return render(request, 'Agent/index.html', context)

def loginPageView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Vous êtes connecté')
                return redirect('home')
        # Authentication failed, display custom error message
        messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    else:
        form = AuthenticationForm()
    return render(request, 'Agent/Login.html', {'form': form})

@admin_only
def registerPageView(request):  
    collaborators = Collaborateur.objects.all()  # Fetch all collaborators
    if request.POST:
        formRegister = registerForm(request.POST)
        if request.POST.get("sign-up"):
            group = request.POST['group']
            name = request.POST['name']  # Retrieve selected collaborator's name
            print(name)
            if formRegister.is_valid():
                # Assuming 'name' is the field for collaborator's name in the form
                formRegister.cleaned_data['name'] = name  # Set the selected name in form data
                if name:
                    try:
                        collaborateur = Collaborateur.objects.get(Nom=name)  # Retrieve collaborator by name
                        user = formRegister.save()
                        user.groups.add(Group.objects.get(name=group))
                        collaborateur.user = user
                        collaborateur.save()
                        messages.info(request, 'Votre compte a été créé avec succès. Veuillez vous connecter.')
                        return redirect('home_admin')
                    except Collaborateur.DoesNotExist:
                        messages.error(request, 'Nom de collaborateur invalide.')   
    else:
        formRegister = registerForm()
    context = {'formRegister': formRegister, 'collaborators': collaborators}
    return render(request, 'admin_/register.html', context)

@login_required(login_url='login')
@admin_only
def Adimn_view(request):
    current_date = datetime.now().date()
    collaborateur_inactif=Collaborateur.objects.filter(Statut='INACTIF').count()
    collaborateur_actif=Collaborateur.objects.filter(Statut='ACTIF').count()
    collaborateur_man=Collaborateur.objects.filter(Sexe='H',Statut='ACTIF').count()
    collaborateur_Women=Collaborateur.objects.filter(Sexe='F',Statut='ACTIF').count()
    collaborateur_france=Collaborateur.objects.filter(Activite='FRANCE',Statut='ACTIF').count()
    collaborateur_canada=Collaborateur.objects.filter(Activite='CANADA',Statut='ACTIF').count()
    salaire_som=0
    for collaborateur in Collaborateur.objects.all():
        if not collaborateur.Date_de_Sortie or collaborateur.Date_de_Sortie.year == current_date.year and collaborateur.Date_de_Sortie.month == current_date.month:
                salaire_som=collaborateur.Salaire_base+ salaire_som

    inactive_agents_this_month=0
    for collaborateur in Collaborateur.objects.filter(Activite="CANADA",Statut="INACTIF"):
        if not collaborateur.Date_de_Sortie or collaborateur.Date_de_Sortie.year == current_date.year and collaborateur.Date_de_Sortie.month == current_date.month:
            inactive_agents_this_month=inactive_agents_this_month + 1
    
    all_agents_this_month = Collaborateur.objects.filter(
    Q(Date_de_Sortie__contains=current_date.month) | Q(Date_de_Sortie__isnull=True)
    )
    total_agents_this_month = all_agents_this_month.count()
    turnover_percentage = round((inactive_agents_this_month / total_agents_this_month) * 100, 2)
    context={
        'collaborateur_Actif':collaborateur_actif,
        'collaborateur_Inactif':collaborateur_inactif,
        'collaborateur_man':collaborateur_man,
        'collaborateur_women':collaborateur_Women,
        'collaborateur_france':collaborateur_france,
        'collaborateur_canada':collaborateur_canada,
        'collaborateur_Turnover':turnover_percentage,
        'salaire_max':salaire_som,
    }
    return render(request,'admin_/home_admin.html',context)

@login_required(login_url='login')
@admin_only
def TableView(request):
    context = Collaborateur.objects.all()
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    nom_query_lower = nom_query.lower() if nom_query else None
    prenom_query_lower = prenom_query.lower() if prenom_query else None
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query_lower) | Q(Prenom__icontains=prenom_query_lower))
    else:
        context= Collaborateur.objects.all()
    return render(request, 'admin_/tables.html', {'collaborateur': context})

@login_required(login_url='login')
@admin_only
def TableViewEv(request):
    context = Event.objects.all()
    return render(request, 'admin_/tables event.html', {'Event': context})

@login_required(login_url='login')
@admin_only
def TableView_Canada(request):
    current_date = datetime.now().date()
    
    month_year_str = current_date.strftime('%B %Y')
    context = Collaborateur.objects.filter(Activite='CANADA')
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query) | Q(Prenom__icontains=prenom_query))
    else:
        context= Collaborateur.objects.filter(Activite='CANADA')
    context2 = Salaire_CANADA.objects.filter(Date_de_salaire__contains=month_year_str)

    return render(request, 'admin_/salaire_complet/Salaries CANADA.html', {'collaborateur': context,'salaire':context2})

@login_required(login_url='login')
@admin_only
def TableView_Paie_Mod_Admin(request):
    current_date = datetime.now()
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    nom_query_lower = nom_query.lower() if nom_query else None
    prenom_query_lower = prenom_query.lower() if prenom_query else None
    first_day_of_month = current_date.replace(day=1)
    context = Collaborateur.objects.filter(Q(CSP='CADRE') | Q(CSP='TECHNICIEN')).filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query_lower) | Q(Prenom__icontains=prenom_query_lower)).filter(Q(CSP='CADRE') | Q(CSP='TECHNICIEN')).filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    else:
        context = Collaborateur.objects.filter(Q(CSP='CADRE') | Q(CSP='TECHNICIEN')).filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    return render(request, 'admin_/salaire_complet/Modif Salaire Admin.html', {'collaborateur': context})

@login_required(login_url='login')
@admin_only
def TableView_Paie_Mod_Cana(request):
    current_date = datetime.now()
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    nom_query_lower = nom_query.lower() if nom_query else None
    prenom_query_lower = prenom_query.lower() if prenom_query else None
    first_day_of_month = current_date.replace(day=1)
    context = Collaborateur.objects.filter(Activite='CANADA').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query_lower) | Q(Prenom__icontains=prenom_query_lower)).filter(Activite='CANADA').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    else:
        context = Collaborateur.objects.filter(Activite='CANADA').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    return render(request, 'admin_/salaire_complet/Modif Salaire Canada.html', {'collaborateur': context})

@login_required(login_url='login')
@admin_only
def TableView_Paie_Mod_Fran(request):
    current_date = datetime.now()
    print(current_date)
    first_day_of_month = current_date.replace(day=1)
    context = Collaborateur.objects.filter(Activite='FRANCE').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    nom_query_lower = nom_query.lower() if nom_query else None
    prenom_query_lower = prenom_query.lower() if prenom_query else None
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query_lower) | Q(Prenom__icontains=prenom_query_lower)).filter(Activite='FRANCE').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    else:
        context = Collaborateur.objects.filter(Activite='FRANCE').filter(Q(Date_de_Sortie__gte=first_day_of_month) | Q(Date_de_Sortie__isnull=True))
    return render(request, 'admin_/salaire_complet/Modif Salaire FRANCE.html', {'Collaborateur': context})

@login_required(login_url='login')
@admin_only
def TableView_France(request):
    current_date = datetime.now().date()
    
    month_year_str = current_date.strftime('%B %Y')
    context = Collaborateur.objects.filter(Activite='FRANCE')
    nom_query = request.GET.get('Nom', '')
    prenom_query = request.GET.get('Nom', '')
    if nom_query or prenom_query:
        context = Collaborateur.objects.filter(Q(Nom__icontains=nom_query) | Q(Prenom__icontains=prenom_query))
    else:
        context= Collaborateur.objects.filter(Activite='FRANCE')
    context2 = Salaire_FRANCE.objects.filter(Date_de_salaire__contains=month_year_str)

    return render(request, 'admin_/salaire_complet/Salaries FRANCE.html', {'collaborateur': context,'salaire':context2})

@login_required(login_url='login')
@admin_only
def AddCView(request):
    if request.method == "POST":
        form = Collaborateurform(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('table')
    if request.method == "GET":
        form = Collaborateurform()
    return render(request,'admin_/addC.html',{'form':form})

@login_required(login_url='login')
@admin_only
def AddEView(request):
    if request.method == "POST":
        form = EventForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tableEV')
    if request.method == "GET":
        form = EventForm()
    return render(request,'admin_/addEV.html',{'form':form})

@login_required(login_url='login')
@admin_only
def Form_EDS_CANADA(request,id):
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')  
    instance= Collaborateur.objects.get(id=id)
    salaire=Salaire_CANADA.objects.get(id_Collaborateur=id,Date_de_salaire=month_year_str)
    if instance:
        return render(request,'admin_/salaire_complet/Form_Canada.html',{'collaborateur':instance,'salaire':salaire})
    return render(request,'admin_/salaire_complet/Salaries CANADA.html')

@login_required(login_url='login')
@admin_only
def Form_EDS_FRANCE(request,id):
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')
    instance= Collaborateur.objects.get(id=id)
    salaire=Salaire_FRANCE.objects.get(id_Collaborateur=id,Date_de_salaire=month_year_str)
    if instance:
        return render(request,'admin_/salaire_complet/Form_France.html',{'collaborateur':instance,'salaire':salaire})
    return render(request,'admin_/salaire_complet/Salaries FRANCE.html')

@login_required(login_url='login')
@admin_only
def EditCView(request,id):
    instance= Collaborateur.objects.get(id=id)
    if request.method == "POST":
        form = Collaborateurform(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('table')
    if request.method == "GET":
        form = Collaborateurform(instance=instance)
    return render(request,'admin_/EditC.html',{'form':form,'collaborateur':instance})

@login_required(login_url='login')
@admin_only
def EditEView(request,id):
    instance= Event.objects.get(id=id)
    if request.method == "POST":
        form = EventForm(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('tableEV')
    if request.method == "GET":
        form = EventForm(instance=instance)
    return render(request,'admin_/EditE.html',{'form':form,'Event':instance})

@login_required(login_url='login')
@admin_only
def EditS_Admin_View(request,id):
    instance= Collaborateur.objects.get(id=id)
    if request.method == "POST":
        form = SalaireFormA(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('ModifSA')
    if request.method == "GET":
        form = SalaireFormA(instance=instance)
    return render(request,'admin_/EditS.html',{'form':form,'collaborateur':instance})

@login_required(login_url='login')
@admin_only
def EditS_Canada_View(request,id):
    instance= Collaborateur.objects.get(id=id)
    if request.method == "POST":
        form = SalaireForm(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('ModifS')
    if request.method == "GET":
        form = SalaireForm(instance=instance)
    return render(request,'admin_/EditS.html',{'form':form,'collaborateur':instance})

@login_required(login_url='login')
@admin_only
def EditS_France_View(request,id):
    instance= Collaborateur.objects.get(id=id)
    if request.method == "POST":
        form = SalaireForm(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('ModifSF')
    if request.method == "GET":
        form = SalaireForm(instance=instance)
    return render(request,'admin_/EditSF.html',{'form':form,'collaborateur':instance})


@login_required(login_url='login')
@admin_only
def DelCView(request,id):
    dele=Collaborateur.objects.get(id=id)
    if request.method == "POST":
        dele.delete()
        return redirect('table')
    context={
            'Collaborateur':dele,
        }
    return render(request,'admin_/delet.html',context)

@login_required(login_url='login')
@admin_only
def DelEView(request,id):
    dele=Event.objects.get(id=id)
    if request.method == "POST":
        dele.delete()
        return redirect('table')
    context={
            'Event':dele,
        }
    return render(request,'admin_/deletEV.html',context)

@login_required(login_url='login')
@admin_only
def DelSView_CA(request,id):
    dele=Collaborateur.objects.get(id=id)
    dele2=Salaire_CANADA.objects.get(id_Collaborateur=dele.id)
    if request.method == "POST":
        dele2.delete()
        return redirect('table')
    context={
            'Collaborateur':dele,
        }
    return render(request,'admin_/deletCA.html',context)

@login_required(login_url='login')
@admin_only
def DelSView_FA(request,id):
    dele=Collaborateur.objects.get(id=id)
    dele2=Salaire_FRANCE.objects.get(id=dele.id)
    if request.method == "POST":
        dele2.delete()
        return redirect('table')
    context={
            'salaire':dele2,
        }
    return render(request,'admin_/delet.html',context)

def logoutview(request):
    logout(request)
    return redirect('home')


def Salaries_calculer(request):
    context = Salaire_CANADA.objects.all()
    if 'Nom' in request.GET and request.GET['Nom']:
        nom_query = request.GET['Nom']
        id=Collaborateur.objects.get(Nom=nom_query)
        context = Salaire_CANADA.objects.filter(id_Collaborateur=id)
    else:
        context = Salaire_CANADA.objects.all()
    return render(request, 'admin_/salaire_complet/tables salaire.html', {'salaire': context})

@admin_only
def Salaries_agent_CANADA(request):
    if request.method == 'POST':
        th_f = float(request.POST['TH'])
        collaborateurs = Collaborateur.objects.filter(CSP='AGENT',Activite='CANADA')
        activate('fr')
        current_date = datetime.now().date()
        month_year_str = current_date.strftime('%B %Y')
        # Check if a salary entry already exists for the current month
        salaries = []  # List to store all Salaire instances
        existing_salaries = Salaire_CANADA.objects.filter(Date_de_salaire=month_year_str)
        # If salary entries already exist for the current month, redirect to another page
        if existing_salaries.exists():
            return redirect('tableC') 
        for collaborateur in collaborateurs:
            if not collaborateur.Date_de_Sortie or collaborateur.Date_de_Sortie.year == current_date.year and collaborateur.Date_de_Sortie.month == current_date.month:  
                th = collaborateur.Salaire_base / th_f
                collaborateur.Planifier=th_f
                salary = round((collaborateur.Nbre_d_heures_Travaillees * th) + collaborateur.Prime_Produit - collaborateur.Avance_sur_salaire,2)
                collaborateur.S_H = round(th,3)
                collaborateur.save()
            # Create a new instance of the Salaire model
                salaire = Salaire_CANADA.objects.create(
                    id_Collaborateur=collaborateur,
                    Date_de_salaire=month_year_str,
                    salaire_finale=round(salary,2),
                    Prime_Produit=collaborateur.Prime_Produit,
                    Nbre_d_heures_Travaillees = collaborateur.Nbre_d_heures_Travaillees,
                    Avance_sur_salaire= collaborateur.Avance_sur_salaire,
                    S_H =round(th,3),
                    Planifier =  th_f,
                )
                salaries.append(salaire)
        context = {
            'collaborateurs': collaborateurs,
            'salaire': salaries,
            'TH_f': th_f,
            'moin': month_year_str
        }
        return render(request, 'admin_/salaire_complet/Salaries CANADA.html', context)
    return render(request, 'admin_/salaire_complet/Salaries CalculeC.html')

@admin_only
def Salaries_agent_FRANCE(request):
    if request.method == 'POST':
        th_f = float(request.POST['TH'])
        collaborateurs = Collaborateur.objects.filter(CSP='AGENT', Activite='FRANCE')
        activate('fr')
        current_date = datetime.now().date()
        month_year_str = current_date.strftime('%B %Y')
        # Check if a salary entry already exists for the current month
        existing_salaries = Salaire_FRANCE.objects.filter(Date_de_salaire=month_year_str)
        # If salary entries already exist for the current month, redirect to another page
        if existing_salaries.exists():
            return redirect('tableF') 
        salaries = []  # List to store all Salaire instances
        for collaborateur in collaborateurs:
            if not collaborateur.Date_de_Sortie or collaborateur.Date_de_Sortie.year == current_date.year and collaborateur.Date_de_Sortie.month == current_date.month:
                th = collaborateur.Salaire_base / th_f
                collaborateur.Planifier = th_f
                salary = round((collaborateur.Nbre_d_heures_Travaillees * th) + collaborateur.Prime_Produit - collaborateur.Avance_sur_salaire, 2)
                collaborateur.S_H = round(th, 3)
                collaborateur.save()
                salaire = Salaire_FRANCE.objects.create(
                    id_Collaborateur=collaborateur,
                    Date_de_salaire=month_year_str,
                    salaire_finale=round(salary, 2),
                    Prime_Produit=collaborateur.Prime_Produit,
                    Nbre_d_heures_Travaillees=collaborateur.Nbre_d_heures_Travaillees,
                    Avance_sur_salaire=collaborateur.Avance_sur_salaire,
                    S_H=round(th, 3),
                    Planifier=th_f,
                )
                salaries.append(salaire)
        context = {
            'collaborateurs': collaborateurs,
            'salaire': salaries,
            'TH_f': th_f,
            'moin': month_year_str
        }
        return render(request, 'admin_/salaire_complet/Salaries FRANCE.html', context)
    return render(request, 'admin_/salaire_complet/Salaries CalculeF.html')

@admin_only
def Salaries_admin(request):
    collaborateurs = Collaborateur.objects.filter(Q(CSP='CADRE') | Q(CSP='TECHNICIEN'))
    activate('fr')
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')
    salaries = []  # List to store all Salaire instances
    existing_salaries = Salaire_admin.objects.filter(Date_de_salaire=month_year_str)
        # If salary entries already exist for the current month, redirect to another page
    if existing_salaries.exists():
        return redirect('rapport Admin') 
    for collaborateur in collaborateurs:
        Days_ofwork= collaborateur.Nombre_de_Jour_Travaille_Admin
        salary = round((collaborateur.Salaire_base / 22) * Days_ofwork-collaborateur.Avance_sur_salaire, 2)
        collaborateur.save()
            # Create a new instance of the Salaire model
        salaire = Salaire_admin.objects.create(
            id_Collaborateur=collaborateur,
            Date_de_salaire=month_year_str,  # You may want to adjust this
            salaire_finale=salary,
        )
        salaries.append(salaire)
    context = {
        'collaborateurs': collaborateurs,
        'salaire': salaries,
        'moin': month_year_str
        }
    return render(request, 'admin_/salaire_complet/Admin_salaire.html', context)

@admin_only
def generate_pdf_CANADA(request,id):
    collaborateur = get_object_or_404(Collaborateur, id=id)
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')
    salaire = Salaire_CANADA.objects.get(id_Collaborateur=id,Date_de_salaire=month_year_str)
    context = {'collaborateur': collaborateur,'salaire':salaire}
    # Render Jinja2 template
    template = get_template('admin_/salaire_complet/Form_Canada.html')
    html = template.render(context)
    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # Convert HTML to PDF
    pdf_content = pdfkit.from_string(html, False, configuration=config)
    # Create an HttpResponse with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="C.pdf"'
    return response

@admin_only
def generate_pdf_FRANCE(request,id):
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')  
    collaborateur = get_object_or_404(Collaborateur, id=id)
    salaire = Salaire_FRANCE.objects.get(id_Collaborateur=id,Date_de_salaire=month_year_str)
    context = {'collaborateur': collaborateur,'salaire':salaire}
    # Render Jinja2 template
    template = get_template('admin_/salaire_complet/Form_France.html')
    html = template.render(context)
    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf='/bin/wkhtmltopdf')
    # Convert HTML to PDF
    pdf_content = pdfkit.from_string(html, False, configuration=config)
    # Create an HttpResponse with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    return response

@admin_only
def Report_salaire_agent_canada(request):
    context2 = Salaire_CANADA.objects.all()
    if 'month' in request.GET and 'Year' in request.GET:
        month = request.GET['month']
        year = request.GET['Year']
        if month:
            if year:
                # Combine month and year to match the format stored in Date_de_salaire field
                month_year = f"{month} {year}"
                context2 = Salaire_CANADA.objects.filter(Date_de_salaire=month_year)
            else:
                # Filter data for the selected month across all years
                context2 = Salaire_CANADA.objects.filter(Date_de_salaire__contains=month)
        elif year:
            # Split the Date_de_salaire field into separate month and year components
            context2 = Salaire_CANADA.objects.filter(Date_de_salaire__contains=year)
    else:
        context2 = Salaire_CANADA.objects.all()
    return render(request, 'admin_/salaire_complet/rapport Agent_CANADA.html', {'salaire': context2})


@admin_only
def Report_salaire_agent_france(request):
    context2 = Salaire_CANADA.objects.all()
    if 'month' in request.GET and 'Year' in request.GET:
        month = request.GET['month']
        year = request.GET['Year']
        if month:
            if year:
                month_year = f"{month} {year}"
                context2 = Salaire_FRANCE.objects.filter(Date_de_salaire=month_year)
            else:
                context2 = Salaire_FRANCE.objects.filter(Date_de_salaire__contains=month)
        elif year:
            context2 = Salaire_FRANCE.objects.filter(Date_de_salaire__contains=year)
    else:
        context2 = Salaire_FRANCE.objects.all()
    return render(request, 'admin_/salaire_complet/rapport Agent_FRANCE.html', {'salaire': context2})

@admin_only
def Report_salaire_admin(request):
    context2 = Salaire_admin.objects.all()
    if 'month' in request.GET and 'Year' in request.GET:
        month = request.GET['month']
        year = request.GET['Year']
        if month:
            if year:
                # Combine month and year to match the format stored in Date_de_salaire field
                month_year = f"{month} {year}"
                context2 = Salaire_admin.objects.filter(Date_de_salaire=month_year)
            else:
                # Filter data for the selected month across all years
                context2 = Salaire_admin.objects.filter(Date_de_salaire__contains=month)
        elif year:
            # Split the Date_de_salaire field into separate month and year components
            context2 = Salaire_admin.objects.filter(Date_de_salaire__contains=year)
    else:
        context2 = Salaire_admin.objects.all()
    return render(request, 'admin_/salaire_complet/rapport Admin.html', {'salaire': context2})

@admin_only
def VirementView(request):
    context = Collaborateur.objects.all()
    context2 = Salaire_CANADA.objects.all()
    context4 = Salaire_FRANCE.objects.all()
    context3 = Salaire_admin.objects.all()
    salaire = list(context2) + list(context3) + list(context4)
    return render(request, 'admin_/salaire_complet/Virement.html', {'collaborateur': context, 'salaire': salaire})

@admin_only
def export_to_csv_Canada(request):
    Canada_salaires = Salaire_CANADA.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Canada_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prenom', 'Salaire/Heure', 'Nbre_d_heures_Travaillees', 'Prime_Produit', 'Avance_sur_salaire','salaire_finale'])
    for salaire in Canada_salaires:
        nom = salaire.id_Collaborateur.Nom  
        prenom = salaire.id_Collaborateur.Prenom 
        taux_horaire = salaire.id_Collaborateur.Nbre_d_heures_Travaillees
        prime_produit = salaire.id_Collaborateur.Prime_Produit
        avance_sur_salaire = salaire.id_Collaborateur.Avance_sur_salaire
        SH = salaire.id_Collaborateur.S_H
        salaire = salaire.salaire_finale
        writer.writerow([nom, prenom, SH , taux_horaire, prime_produit, avance_sur_salaire,salaire])
    return response

@admin_only
def export_to_csv_France(request):
    Canada_salaires = Salaire_FRANCE.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Canada_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prenom', 'Salaire/Heure', 'Nbre_d_heures_Travaillees', 'Prime_Produit', 'Avance_sur_salaire','salaire_finale'])
    for salaire in Canada_salaires:
        nom = salaire.id_Collaborateur.Nom  
        prenom = salaire.id_Collaborateur.Prenom 
        taux_horaire = salaire.Nbre_d_heures_Travaillees
        prime_produit = salaire.Prime_Produit
        avance_sur_salaire = salaire.Avance_sur_salaire
        SH = salaire.S_H
        salaire = salaire.salaire_finale
        writer.writerow([nom, prenom, SH , taux_horaire, prime_produit, avance_sur_salaire,salaire])
    return response

@admin_only
def modify_salary_CANADA(request):
    if request.method == 'GET':
        activate('fr')
        current_date = datetime.now()
        month_year_str = current_date.strftime('%B %Y')        
        collaborateurs = Collaborateur.objects.filter(Activite='CANADA')
        salaires = Salaire_CANADA.objects.filter(Date_de_salaire=month_year_str)
        for c in collaborateurs:
            try:
                salaire = salaires.get(id_Collaborateur=c.id)             
                salaire_f = c.S_H * c.Nbre_d_heures_Travaillees + c.Prime_Produit - c.Avance_sur_salaire
                salaire.salaire_finale = round(salaire_f,2)
                salaire.Prime_Produit=c.Prime_Produit
                salaire.Avance_sur_salaire=c.Avance_sur_salaire
                salaire.Nbre_d_heures_Travaillees=c.Nbre_d_heures_Travaillees
                salaire.save()
            except Salaire_CANADA.DoesNotExist:
                pass
                
        return redirect('tableC')
    
    return redirect('ModifSC')

@admin_only
def modify_salary_France(request):
    if request.method == 'GET':
        activate('fr')
        current_date = datetime.now()
        month_year_str = current_date.strftime('%B %Y')        
        collaborateurs = Collaborateur.objects.filter(Activite='FRANCE')
        salaires = Salaire_FRANCE.objects.filter(Date_de_salaire=month_year_str)
        for c in collaborateurs:
            try:
                salaire = salaires.get(id_Collaborateur=c.id)
                salaire_f = round(c.S_H * c.Nbre_d_heures_Travaillees + c.Prime_Produit - c.Avance_sur_salaire,2)
                print(salaire_f)
                salaire.salaire_finale = salaire_f
                salaire.Prime_Produit=c.Prime_Produit
                salaire.Avance_sur_salaire=c.Avance_sur_salaire
                salaire.Nbre_d_heures_Travaillees=c.Nbre_d_heures_Travaillees
                salaire.save()
            except Salaire_FRANCE.DoesNotExist:
                pass
        return redirect('tableF')
    return redirect('ModifSF')

def import_csv_and_update_agentsF(request):
    if request.method == 'POST':
        if request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            print("File uploaded successfully:", excel_file.name)
            df = pd.read_excel(excel_file, engine='openpyxl')
            print("Excel file read successfully.")
            for index, row in df.iterrows():    
                N = row['Nom']
                P = row['Prénom']   
                if not pd.isna(N):
                    N = N.strip()
                if not pd.isna(P):
                    P = P.strip()
                try:
                    agent = Collaborateur.objects.get(Nom=N, Prenom=P)
                except Collaborateur.DoesNotExist:
                    messages.warning(request, f'Agent with nom {N} and prenom {P} not found.')
                    continue
                realise_h = row['H Réalisé']
                Prime=row['Prime PROD']
                Avance=row['Avance sur salaire']    
                if pd.isna(Prime):
                    Prime = 0
                if pd.isna(Avance):
                    Avance = 0
                agent.Nbre_d_heures_Travaillees = realise_h
                agent.Prime_Produit=Prime
                agent.Avance_sur_salaire=Avance
                agent.save()
                print("Agent data updated:", agent)
            messages.success(request, 'Agent data updated successfully.')
        else:
            print("No file uploaded.")
    return redirect('ModifSF')

def import_csv_and_update_agentsC(request):
    if request.method == 'POST':
        if request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file, engine='openpyxl')
            for index, row in df.iterrows():    
                N = row['Nom']
                P = row['Prénom']   
                if not pd.isna(N):
                    N = N.strip()
                if not pd.isna(P):
                    P = P.strip() 
                try:
                    agent = Collaborateur.objects.get(Nom=N, Prenom=P)
                except Collaborateur.DoesNotExist:
                    messages.warning(request, f'Agent with nom {N} and prenom {P} not found.')
                    continue
                realise_h = row['H Réalisé']
                Prime = row['Prime PROD']
                Avance = row['Avance sur salaire']
                if pd.isna(Prime):
                    Prime = 0
                if pd.isna(Avance):
                    Avance = 0
                agent.Nbre_d_heures_Travaillees = realise_h
                agent.Prime_Produit = Prime
                agent.Avance_sur_salaire = Avance
                agent.save()
            messages.success(request, 'Agent data updated successfully.')
        else:
            print("No file uploaded.")

    return redirect('ModifSC')

@login_required(login_url='login')
def userPage(request):
    collaborateur = Collaborateur.objects.get(user=request.user)
    context = {'collaborateur':collaborateur}
    return render(request, 'Agent/compte.html', context)

@login_required(login_url='login')
def Tiquet(request):
    return render(request, 'Agent/Tiquet.html')
