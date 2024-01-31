from django.urls import path,include
from . import views
urlpatterns = [
    #home
  path('', views.IndexView.as_view(), name='home'),
]
