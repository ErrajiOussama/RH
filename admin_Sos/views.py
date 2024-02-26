from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from admin_Sos.models import *
from admin_Sos.forms import *
from .decorators import *
from datetime import datetime
from django.utils.translation import activate
from django.template.loader import get_template
from .filter import * 
from django.shortcuts import get_object_or_404
import jinja2
import pdfkit

@login_required(login_url='login')
def IndexView(request):
    return render(request,'Agent/index.html')


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
    return render(request, 'Agent/login.html', {'form': form})

@admin_only
def registerPageView(request):    
    if request.POST:
        formRegister = registerForm(request.POST)
        if request.POST.get("sign-up"):
            group=request.POST['group']
            if formRegister.is_valid():
                id = formRegister.cleaned_data.get('id')
                if id:
                    try:
                        collaborateur = Collaborateur.objects.get(id=id)
                        user = formRegister.save()
                        
                        user.groups.add(Group.objects.get(name=group))
                        collaborateur.user = user
                        collaborateur.save()
                        messages.info(request, 'Votre compte a été créé avec succès. Veuillez vous connecter.')
                        return redirect('home_admin')
                    except Collaborateur.DoesNotExist:
                        messages.error(request, 'Collaborateur ID invalide.')   
    else:
        formRegister = registerForm()
    context = {'formRegister' : formRegister}
    return render(request, 'admin_/register.html', context )

@login_required(login_url='login')
@admin_only
def Adimn_view(request):
    collaborateur_inactif=Collaborateur.objects.filter(Statut='INACTIF').count()
    collaborateur_actif=Collaborateur.objects.filter(Statut='ACTIF').count()
    collaborateur_man=Collaborateur.objects.filter(Sexe='H').count()
    collaborateur_Women=Collaborateur.objects.filter(Sexe='F').count()
    c=1
    collaborateur1=Collaborateur.objects.get(id=1)
    salaire_som=collaborateur1.Salaire_base
    for collaborateur in Collaborateur.objects.all():
        if c > 1 :
            salaire_som=collaborateur.Salaire_base+ salaire_som
        c=c+1 
    collaborateur_Turnover= round((Collaborateur.objects.filter(Statut='INACTIF').count()/Collaborateur.objects.all().count())*100, 2)
    
    context={
        'collaborateur_Actif':collaborateur_actif,
        'collaborateur_Inactif':collaborateur_inactif,
        'collaborateur_man':collaborateur_man,
        'collaborateur_women':collaborateur_Women,
        'collaborateur_Turnover':collaborateur_Turnover,
        'salaire_max':salaire_som,
    }
    return render(request,'admin_/home_admin.html',context)

@login_required(login_url='login')
@admin_only
def TableView(request):
    context = Collaborateur.objects.all()
    myFilter = Cola_filter(request.GET, queryset=context)

    if 'Nom' in request.GET and request.GET['Nom']:
        nom_query = request.GET['Nom']
        context = Collaborateur.objects.filter(Nom=nom_query)
    else:
        context = myFilter.qs

    return render(request, 'admin_/tables.html', {'collaborateur': context, 'myFilter': myFilter})

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
def Form_EDS(request,id):
    instance= Collaborateur.objects.get(id=id)
    salaire=Salaire.objects.get(id_Collaborateur=id)
    if instance:
        return render(request,'admin_/salaire_complet/Form.html',{'collaborateur':instance,'salaire':salaire})
    return render(request,'admin_/salaire_complet/Salaries.html')

@login_required(login_url='login')
@admin_only
def EditCView(request,id):
    instance= Collaborateur.objects.get(id=id)
    if request.method == "POST":
        form = Collaborateurform(data=request.POST,files=request.FILES,instance=instance)
        if form.is_valid:
            form.save()
            return redirect('table')
    if request.method == "GET":
        form = Collaborateurform(instance=instance)
    return render(request,'admin_/EditC.html',{'form':form,'collaborateur':instance})

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

def logoutview(request):
    logout(request)
    return redirect('home')


def Salaries_calculer(request):
    context = Salaire.objects.all()

    myFilter = Cola_filter(request.GET, queryset=context)
    if 'Nom' in request.GET and request.GET['Nom']:
        nom_query = request.GET['Nom']
        id=Collaborateur.objects.get(Nom=nom_query)
        context = Salaire.objects.filter(id_Collaborateur=id)
    else:
        context = Salaire.objects.all()

    return render(request, 'admin_/salaire_complet/tables salaire.html', {'salaire': context})

@admin_only
def modify_salary(request,id):
    if request.method == 'GET':
        
        collaborateurs = Collaborateur.objects.get(id=id)
        salaire=Salaire.objects.get(id_Collaborateur=id)
        activate('fr')
        current_date = datetime.now()
        month_year_str = current_date.strftime('%B %Y')
        # Check if a salary entry already exists for the current month

        hours_of_work = collaborateurs.Taux_Horaire
        prime = collaborateurs.Prime_Produit
        PrimeAvance = collaborateurs.Avance_sur_salaire
        salary = round(hours_of_work * collaborateurs.S_H + prime - PrimeAvance, 2)
        salaire.salaire_finale=salary
        salaire.Date_de_salaire=month_year_str
        salaire.save()
        
    
    return redirect('rapport Agent')

@admin_only
def Salaries_agent(request):
    if request.method == 'POST':
        th_f = float(request.POST['TH'])
        collaborateurs = Collaborateur.objects.filter(CSP='AGENT')
        activate('fr')
        current_date = datetime.now().date()
        month_year_str = current_date.strftime('%B %Y')
        second_month_date = datetime(current_date.year, 2, 1).date()
        
        # Check if a salary entry already exists for the current month

        salaries = []  # List to store all Salaire instances
        existing_salaries = Salaire.objects.filter(Date_de_salaire=month_year_str)

        # If salary entries already exist for the current month, redirect to another page
        if existing_salaries.exists():
            return redirect('rapport Agent') 
        for collaborateur in collaborateurs:
            if collaborateur.Date_de_Sortie and collaborateur.Date_de_Sortie < second_month_date:
                # Skip calculation if Date_de_Sortie is before the second month
                continue
            th = round(collaborateur.Salaire_base / th_f, 2)
            hours_of_work = collaborateur.Taux_Horaire
            prime = collaborateur.Prime_Produit
            PrimeAvance = collaborateur.Avance_sur_salaire
            collaborateur.Planifier=th_f
            salary = round(hours_of_work * th + prime - PrimeAvance, 2)
            collaborateur.S_H = th
            collaborateur.save()
            
            # Create a new instance of the Salaire model
            salaire = Salaire.objects.create(
                id_Collaborateur=collaborateur,
                Date_de_salaire=month_year_str,
                salaire_finale=salary,
            )
            salaries.append(salaire)
        
        context = {
            'collaborateurs': collaborateurs,
            'salaire': salaries,
            'TH_f': th_f,
            'moin': month_year_str
        }
        return render(request, 'admin_/salaire_complet/salary_result.html', context)
    return render(request, 'admin_/salaire_complet/Salaries.html')

@admin_only
def Salaries_admin(request):
    collaborateurs = Collaborateur.objects.filter(Poste='CADRE')
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

"""
def generate_pdf(request, id):
    collaborateur = get_object_or_404(Collaborateur, id=id)
        # Rendered template with collaborateur data
    template = get_template('admin_/Form.html')
    context = {'collaborateur': collaborateur}  # Pass the collaborateur object to the context
    html = template.render(context)

        # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # Generate PDF
    from xhtml2pdf import pisa
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
"""


@admin_only
def generate_pdf(request,id):
    
    collaborateur = get_object_or_404(Collaborateur, id=id)
    salaire = Salaire.objects.get(id_Collaborateur=id)
    context = {'collaborateur': collaborateur,'salaire':salaire}

    # Render Jinja2 template
    template = get_template('admin_/salaire_complet/Form.html')
    html = template.render(context)
    
    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    # Convert HTML to PDF
    pdf_content = pdfkit.from_string(html, False, configuration=config)

    # Create an HttpResponse with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    
    return response

@admin_only
def Report_salaire_agent(request):
    context = Collaborateur.objects.filter(Poste='Agent')
    context2 = Salaire.objects.all()
    
    if 'group' in request.GET and request.GET['group']:
        group=request.GET['group']
        
        context2 = Salaire.objects.filter(Date_de_salaire=group)

    return render(request, 'admin_/salaire_complet/rapport Agent.html', {'collaborateur': context,'salaire': context2})
@admin_only
def Report_salaire_admin(request):
    context = Collaborateur.objects.filter(Poste='Admin')
    context2 = Salaire_admin.objects.all()
    
    
    if 'group' in request.GET and request.GET['group']:
        group=request.GET['group']
        context2 = Salaire_admin.objects.filter(Date_de_salaire=group)

    return render(request, 'admin_/salaire_complet/rapport Admin.html', {'collaborateur': context,'salaire': context2})
@admin_only
def VirementView(request):
    context = Collaborateur.objects.all()
    context2 = Salaire.objects.all()
    context3 = Salaire_admin.objects.all()

    salaire = list(context2) + list(context3)

    return render(request, 'admin_/salaire_complet/Virement.html', {'collaborateur': context, 'salaire': salaire})

@admin_only
def enter_hours(request):
    if request.method == 'POST':
        form = HoursWorkedForm(request.POST)
        if form.is_valid():
            # Process the form data
            for collaborateur in Collaborateur.objects.filter(Poste='Agent'):
                hours_worked = form.cleaned_data.get('hours_worked_{}'.format(collaborateur.id))
                if hours_worked is not None:
                    collaborateur.Taux_Horaire = hours_worked  # Update Taux_Horaire with hours worked
                    collaborateur.save()  # Save collaborateur object with updated Taux_Horaire
            # Redirect or display a success message
            return redirect('table')  # Assuming 'table' is the name of the URL pattern to redirect to
    else:
        form = HoursWorkedForm()
    return render(request, 'admin_/HW.html', {'form': form})