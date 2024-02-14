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
  path('AddC/',views.AddCView,name="AddC"),
  path('EditC/<int:id>',views.EditCView,name="EditC"),
  path('DelC/<int:id>',views.DelCView,name="DelC"),
  path('Salaire/',views.Salaries ,name="salaire"),
]
