from django.urls import path
from . import views
from django.views.generic import ListView, DetailView, DeleteView
from .models import Activite


app_name = 'activite'

urlpatterns = [
    path('', views.activite, name="activite"),
    path('add/', views.addActivite, name='addactivite'),
    path('list_activites/', ListView.as_view(model=Activite), name='list_activites'),
    path('activite/<int:pk>', views.editActivite, name='edit_activite'),
    path('activite_delete/<int:pk>',DeleteView.as_view(model=Activite, success_url='/activite/list_activites'), name="delete_activite"),
    path('test/', views.test,name='test'),
    path('get_eleve/', views.get_eleve, name='get_eleve'),
    path('articles/', views.articles, name='articles'),

]