from django.urls import path,include
from . import views
urlpatterns = [
    #home
  path('', views.IndexView, name='home'),
  path('Login/',views.loginPageView,name='login'),
  path('register/',views.registerPageView,name="register"),
  path('logout/',views.logoutview,name='logout'),
  path('home_admin/',views.Adimn_view,name='home_admin'),
  path('table/',views.TableView ,name="table"),
  path('Virement/',views.VirementView ,name="virement"),
  path('HW/',views.enter_hours ,name="HW"), 
  path('editPrime/',views.enter_primes ,name="editPrime"),
  path('rapport Agent/',views.Report_salaire_agent ,name="rapport Agent"),
  path('rapport Admin/',views.Report_salaire_admin ,name="rapport Admin"),
  path('AddC/',views.AddCView,name="AddC"),
  path('EDS/<int:id>',views.Form_EDS ,name="EDS"),
  path('EditC/<int:id>',views.EditCView,name="EditC"),
  path('DelC/<int:id>',views.DelCView,name="DelC"),
  path('Salaire Agent/',views.Salaries_agent ,name="salaire_agent"),
  path('Salaire Modifier',views.Salaries_calculer ,name="salaire modif"),
  path('Salaire Modifier/<int:id>',views.modify_salary ,name="salaire result"),
  path('Salaire Admin/',views.Salaries_admin ,name="salaire_admin"),
  path('generate_pdf/<int:id>', views.generate_pdf, name='generate_pdf'),
]
