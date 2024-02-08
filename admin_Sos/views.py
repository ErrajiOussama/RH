from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from admin_Sos.models import *
from admin_Sos.forms import *
from django.utils import timezone
from .decorators import * 


class IndexView(View):
    def get(self,request):
        return render(request,'Agent/index.html')
    

@unauthenticated_user
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

@unauthenticated_user
def registerPageView(request):    
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.info(request, 'Vous avez créé votre compte, veuillez vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'admin_/register.html', context)

@allowed_users(allowed_roles=['Admin'])
class AdminView(View):
    def get(self,request):
        collaborateur=Collaborateur.objects.all().count()
        context={
            'collaborateur':collaborateur,
        }
        return render(request,'admin_/home_admin.html',context)

@allowed_users(allowed_roles=['Admin'])
class TableView(View):
    def get(self,request):
        collaborateur=Collaborateur.objects.all()
        context={
            'collaborateur':collaborateur,     
        }
        return render(request,'admin_/tables.html',context)

@allowed_users(allowed_roles=['Admin'])
def AddCView(request):
        if request.method == "POST":
            form = Collaborateurform(data=request.POST,files=request.FILES)
            if form.is_valid:
                form.save()
                return redirect('table')
        if request.method == "GET":
            form = Collaborateurform()
        return render(request,'admin_/addC.html',{'form':form})

@allowed_users(allowed_roles=['Admin'])
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

@allowed_users(allowed_roles=['Admin'])
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


def chrono_view(request):
    if request.method == 'POST':
        start_time = timezone.now()
        stop_time = timezone.now()  # You may need to modify this logic depending on your requirements
        elapsed_time = stop_time - start_time
        chrono_data = Collaborateur.objects.create(start_time=start_time, stop_time=stop_time, elapsed_time=elapsed_time)
        chrono_data.save()
        return redirect('chrono')  # Redirect to the chrono page after saving the data
    return render(request, 'Agent/chrono.html')