from  django.urls import path, include
from . import views
from django.views.generic import ListView, UpdateView
from .models import Enfant, Parent
from django.contrib.auth.decorators import login_required
from .forms import ParentForm

app_name = 'famille'

urlpatterns =[
    path('parent/', login_required(views.parent), name='parent'),
    path('enfant/', views.enfant, name='enfant'),
    path('famille/', views.famille, name='famille'),
    path('enfants/', ListView.as_view(model=Enfant, extra_context={'titre':'Liste des enfants'}), name='enfants'),
    path('parents/',ListView.as_view(model=Parent, extra_context={'titre':'Liste des parents'}), name='parents'),
    path('edit_parent/<int:pk>', UpdateView.as_view(model=Parent,form_class=ParentForm, template_name='famille/parent.html', extra_context={'titre': 'Maj Parent'}), name='edit_parent'),
    path('enfant/<int:pk>', views.userDetail, name='enfantDetail'),
    #path('update_eleve/<int:pk>',UpdateView.as_view(model=Enfant, fields='__all__',success_url='/famille/enfants/'), name='update_eleve'),
    #path('update_eleve/<int:pk>',views.update_eleve, name='update_eleve'),
    path('update_eleve/<int:pk>',views.UpdateEleve.as_view(), name="update_eleve"),
    path('add_enfant_ajax/', views.add_enfant_ajax, name='add_enfant_ajax'),
    path('searchParent/', views.searchParent, name='searchParent'),
]