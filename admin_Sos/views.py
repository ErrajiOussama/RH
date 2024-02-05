from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import *
from admin_Sos.models import *
from admin_Sos.forms import *

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    

def loginPageView(request):
    return render(request, 'Login.html')  

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