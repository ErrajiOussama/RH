from django.shortcuts import render
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    

def loginPageView(request):
    return render(request, 'Login.html')  

class AdminView(View):
    def get(self,request):
        return render(request,'admin_/home_admin.html')
    
class TableView(View):
    def get(self,request):
        Collaborateur=Collaborateur.objects.all()
        context={
            'collaborateur':Collaborateur,     
        }
        return render(request,'admin_/tables.html',context)