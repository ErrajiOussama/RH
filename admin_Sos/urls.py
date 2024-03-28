from django.urls import path,include
from . import views
urlpatterns = [
  #ADMIN_URL
  path('', views.IndexView, name='home'),
  path('Login/',views.loginPageView,name='login'),
  path('register/',views.registerPageView,name="register"),
  path('logout/',views.logoutview,name='logout'),
  path('home_admin/',views.Adimn_view,name='home_admin'),
  path('table/',views.TableView ,name="table"),
  path('table France/',views.TableView_France ,name="tableF"),
  path('table Canada/',views.TableView_Canada ,name="tableC"),
  path('Virement/',views.VirementView ,name="virement"),
  path('rapport Agent Canada/',views.Report_salaire_agent_canada ,name="rapport Agent Canada"),
  path('rapport Agent France/',views.Report_salaire_agent_france ,name="rapport Agent France"),
  path('rapport Admin/',views.Report_salaire_admin ,name="rapport Admin"),
  path('AddC/',views.AddCView,name="AddC"),
  path('EDS CANADA/<int:id>',views.Form_EDS_CANADA ,name="EDSCanada"), 
  path('EDS FRANCE/<int:id>',views.Form_EDS_FRANCE ,name="EDSFrance"), 
  path('EditC/<int:id>',views.EditCView,name="EditC"),
  path('DelC/<int:id>',views.DelCView,name="DelC"),
  path('EditS/<int:id>',views.EditS_Canada_View,name="EditSC"),
  path('EditS/<int:id>',views.EditS_France_View,name="EditSF"),
  path('DelCa/<int:id>',views.DelSView_CA,name="DelCa"),
  path('DelFa/<int:id>',views.DelSView_FA,name="DelFa"),
  path('Salaire Agent Canada/',views.Salaries_agent_CANADA ,name="CalculeC"),
  path('Salaire Agent France/',views.Salaries_agent_FRANCE ,name="CalculeF"),
  path('Modif Salaire Agent Canada/',views.TableView_Paie_Mod_Cana ,name="ModifSC"),
  path('Modif Salaire Agent France/',views.TableView_Paie_Mod_Fran ,name="ModifSF"),
  path('Salaire Agent France/',views.Salaries_agent_FRANCE ,name="CalculeF"),
  path('Salaire Admin/',views.Salaries_admin ,name="salaire_admin"),
  path('generate_pdf/<int:id>', views.generate_pdf_CANADA, name='generate_pdf_Canada'),
  path('generate_pdf_france/<int:id>', views.generate_pdf_FRANCE, name='generate_pdf_France'),
  path('CSV', views.export_to_csv_Canada, name='CSV_CANADA'),
  path('CSV', views.export_to_csv_France, name='CSV_FRANCE'),
  path('Recalculer', views.modify_salary_CANADA, name='Recalculer'),
  path('RecalculerF', views.modify_salary_France, name='RecalculerF'),
  path('ImportF', views.import_csv_and_update_agentsF, name='ImportF'),
  path('ImportC', views.import_csv_and_update_agentsC, name='ImportC'),
  #AGENT URLS
  path('Userpage', views.userPage, name='Userpage'),
]
