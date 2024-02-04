from django.urls import path,include
from . import views
urlpatterns = [
    #home
  path('', views.IndexView.as_view(), name='home'),
  path('Login/',views.loginPageView,name='login'),
  path('home_admin/',views.AdminView.as_view(),name='home_admin'),
  path('table/',views.TableView.as_view(),name="table"),
]
