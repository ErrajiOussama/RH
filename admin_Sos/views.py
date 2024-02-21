from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .forms import *
from admin_Sos.models import *
from admin_Sos.forms import *
from .decorators import *
from datetime import datetime
from django.utils.translation import activate
from django.template.loader import get_template
from .filter import * 
from django.shortcuts import get_object_or_404


@login_required(login_url='login')
def IndexView(request):
    return render(request,'Agent/index.html')


def loginPageView(request):    
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            messages.info(request, 'Vous ete connecter')
            return redirect('home')
    else:
        formRegister = registerForm()
    context = {'formRegister' : formRegister}
    return render(request, 'Agent/login.html', context )

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

    salaire_som=0
    for collaborateur in Collaborateur.objects.all():
        salaire_som=collaborateur.Salaire_base
    collaborateur_Turnover= round((Collaborateur.objects.filter(Statut='INACTIF').count()/Collaborateur.objects.all().count())*100, 2)
    print(collaborateur_man)
    print(collaborateur_Women)
    
    context={
        'collaborateur_Actif':collaborateur_actif,
        'collaborateur_Inactif':collaborateur_inactif,
        'collaborateur_man':collaborateur_man,
        'collaborateur_women':collaborateur_Women,
        'collaborateur_Turnover':collaborateur_Turnover,
        'salaire max':salaire_som,
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
        if form.is_valid:
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
        return render(request,'admin_/Form.html',{'collaborateur':instance,'salaire':salaire})
    return render(request,'admin_/Salaries.html')

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
    return render(request,'admin_/content/delet.html',context)

def logoutview(request):
    logout(request)
    return redirect('home')
""""
@login_required(login_url='login')
def chrono_view(request):
    if request.method == 'POST':
        start_time = timezone.now()
        stop_time = timezone.now()  # You may need to modify this logic depending on your requirements
        elapsed_time = stop_time - start_time
        chrono_data = Collaborateur.objects.create()
        chrono_data.save()
        return redirect('chrono')  # Redirect to the chrono page after saving the data
    return render(request, 'Agent/chrono.html')
"""


"""
def Salaries(request):
    if request.method == 'POST':
        th_f = float(request.POST['TH'])
        collaborateurs = Collaborateur.objects.filter(Poste='Agent')  # Assuming 'post' is a field in your Collaborateur model
        activate('fr')
        # Get the current date
        current_date = datetime.now()
        # Get the name of the current month in French
        month_name = current_date.strftime('%B')
        for collaborateur in collaborateurs:
            print(collaborateur.Nom)
            
            th = round(collaborateur.Salaire_base / th_f, 2)
            hours_of_work = collaborateur.Taux_Horaire  # Assuming 'Horaire' is the hours of work for each collaborateur
            prime = collaborateur.Prime  # Assuming 'Prime' is the prime for each collaborateur
            PrimeAvance = collaborateur.Salaire_Avancee
            print(th)
            # Calculate the salary for this collaborateur
            salary = round(hours_of_work * th + prime - PrimeAvance, 2)
            collaborateur.S_H = th
            # Update the collaborateur object with the calculated salary
            collaborateur.salaire_finale = salary  # Assuming you have a field 'salaire' in your Collaborateur model
            collaborateur.save()
            print(collaborateur.salaire_finale)
        context = {
            'collaborateur': collaborateurs,
            'TH_f': th_f,
            'moin': month_name
        }
        return render(request, 'admin_/salary_result.html', context)
    return render(request, 'admin_/Salaries.html')
"""
@admin_only
def Salaries_agent(request):
    if request.method == 'POST':
        th_f = float(request.POST['TH'])
        collaborateurs = Collaborateur.objects.filter(Poste='Agent')
        activate('fr')
        current_date = datetime.now()
        month_year_str = current_date.strftime('%B %Y')
        existing_salaries = Salaire.objects.filter(Date_de_salaire=month_year_str)

        # If salary entries already exist for the current month, redirect to another page
        if existing_salaries.exists():
            return redirect('home_admin')  # Replace 'other_page_name' with the name of your other page URL pattern

        # Check if a salary entry already exists for the current month

        salaries = []  # List to store all Salaire instances
        for collaborateur in collaborateurs:
            th = round(collaborateur.Salaire_base / th_f, 2)
            hours_of_work = collaborateur.Taux_Horaire
            prime = collaborateur.Prime_Produit
            PrimeAvance = collaborateur.Avance_sur_salaire
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
        return render(request, 'admin_/salary_result.html', context)
    return render(request, 'admin_/Salaries.html')

@admin_only
def Salaries_admin(request):
    collaborateurs = Collaborateur.objects.filter(Poste='Admin')
    activate('fr')
    current_date = datetime.now()
    month_year_str = current_date.strftime('%B %Y')
    salaries = []  # List to store all Salaire instances
    for collaborateur in collaborateurs:
        Days_ofwork= collaborateur.Nombre_de_Jour_Travaille_Admin
        salary = round((collaborateur.Salaire_base / 22) * Days_ofwork, 2)
        print(salary)
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
    return render(request, 'admin_/Admin_salaire.html', context)

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

import jinja2
import pdfkit

def generate_pdf(request, id):
    collaborateur = get_object_or_404(Collaborateur, id=id)
    context = {'collaborateur': collaborateur}

    # Render Jinja2 template
    template = get_template('admin_/Form.html')
    html = template.render(context)
    
    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    # Convert HTML to PDF
    pdf_content = pdfkit.from_string(html, False, configuration=config)

    # Create an HttpResponse with PDF content
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    
    return response


def Report_salaire(request):
    context = Collaborateur.objects.all()
    context2 = Salaire.objects.all()
    
    if 'group' in request.GET and request.GET['group']:
        group=request.GET['group']
        print(group)
        context2 = Salaire.objects.filter(Date_de_salaire=group)

    return render(request, 'admin_/rapport.html', {'collaborateur': context,'salaire': context2})