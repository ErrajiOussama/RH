from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import *
from admin_Sos.models import *
from admin_Sos.forms import *
from django.utils import timezone

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'Agent/index.html')
    


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("good")
        if user is not None:
            print("good_123")
            login(request, user)
            print("good")
            if Collaborateur.objects.get(Poste='admin'):
                # Redirect to a success page
                return redirect('home_admin')
            if Collaborateur.objects.get(Poste='agent'):
                # Redirect to a success page
                return redirect('home')
        else:
            # Display an error message
            messages.error(request, 'Invalid Log or password.')
            return redirect('login')
    else:
        return render(request, 'Agent/login.html')

class AdminView(View):
    def get(self,request):
        collaborateur=Collaborateur.objects.all().count()
        context={
            'collaborateur':collaborateur,
        }
        return render(request,'admin_/home_admin.html',context)
    
class TableView(View):
    def get(self,request):
        collaborateur=Collaborateur.objects.all()
        context={
            'collaborateur':collaborateur,     
        }
        return render(request,'admin_/tables.html',context)

def AddCView(request):
        if request.method == "POST":
            form = Collaborateurform(data=request.POST,files=request.FILES)
            if form.is_valid:
                form.save()
                return redirect('table')
        if request.method == "GET":
            form = Collaborateurform()
        return render(request,'admin_/addC.html',{'form':form})

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