from django.urls import path
from . import views
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Role, Profil
from django.forms import TextInput


app_name = 'user'

urlpatterns = [
    path('add_user/', views.user, name='userprofil'),
    path('role/',views.role, name='role'),
    path('add_role/', views.RoleView.as_view(), name='add_role'),
    path('roles/',ListView.as_view(model=Role, extra_context={'titre':'Liste des roles'}), name='roles'),
    path('role_delete/<int:pk>',DeleteView.as_view(model=Role, success_url='/user/roles/'),name='role_delete' ),
    #path('edit_role/<int:pk>', UpdateView.as_view(model=Role, fields='__all__',extra_context={'titre':'Editon d\'un role'}), name='edit_role'),
    path('edit_role/<int:pk>', views.RoleUpdateView.as_view(), name='edit_role'),
    path('edit/<int:pk>',views.role, name='edit'),
    path('editprofil/', views.profil, name='editprofil'),
    path('listuser/', views.listuser, name='listuser'),
    path('user_delete/<int:pk>',DeleteView.as_view(model=User, success_url='/user/listuser/'),name='user_delete' ),
    path('',login_required(views.profil), name='default')

]
