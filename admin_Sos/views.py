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
from .filter import * 

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
    print(collaborateur_man)
    print(collaborateur_Women)
    
    context={
        'collaborateur_Actif':collaborateur_actif,
        'collaborateur_Inactif':collaborateur_inactif,
        'collaborateur_man':collaborateur_man,
        'collaborateur_women':collaborateur_Women,
    }
    return render(request,'admin_/home_admin.html',context)

@login_required(login_url='login')
@admin_only
def TableView(request):
    context = Collaborateur.objects.all()
    myFilter = Cola_filter(request.GET,queryset=context)
    context=myFilter.qs
    if 'id' in request.GET:
        nom_query = request.GET['id']
        context = Collaborateur.objects.filter(id=nom_query)
    else:
        context = Collaborateur.objects.all()
    
    return render(request, 'admin_/tables.html', {'collaborateur': context, 'myFilter':myFilter,})

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
    if instance:
        Nom=instance.Nom
        Prenom=instance.Prenom
    return render(request,'admin_/Form.html',{'Nom':Nom , 'Prenom':Prenom})

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
    dele.delete()
    cola=Collaborateur.objects.all()
    context={
            'collaborateur':cola,
        }
    return render(request,'admin_/tables.html',context)

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
@admin_only
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
            
            th = collaborateur.Salaire_base/th_f
            hours_of_work = collaborateur.Taux_Horaire  # Assuming 'Horaire' is the hours of work for each collaborateur
            prime = collaborateur.Prime  # Assuming 'Prime' is the prime for each collaborateur
            PrimeAvance=collaborateur.Salaire_Avancee
            print(th)
            # Calculate the salary for this collaborateur
            salary = hours_of_work * th + prime -PrimeAvance
            collaborateur.S_H = th
           # Update the collaborateur object with the calculated salary
            collaborateur.salaire_finale = salary  # Assuming you have a field 'salaire' in your Collaborateur model
            collaborateur.save()
            print(collaborateur.salaire_finale)
        context = {
            'collaborateur': collaborateurs,
            'TH_f': th_f,
            'moin' : month_name
        }
        return render(request, 'admin_/salary_result.html', context)
    return render(request, 'admin_/Salaries.html')
