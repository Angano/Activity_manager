from django.urls import path
from . import views
from django.views.generic import ListView, DetailView, UpdateView
from .models import Facture, Brouillon, Ligne
from .forms import LigneForm, FactureSoldeForm

app_name = 'comptabilite'

urlpatterns = [
    path('',views.comptabilite, name='comptabilite'),
    path('encaissement/',views.validation_pointage, name='encaissement'),
    path('relance/',views.relance, name='relance'),
    path('validation_pointage/',views.validation_pointage, name='validation_pointage'),
    path('brouillons/', views.brouillons, name='brouillons'),
    path('factures/',ListView.as_view(model=Facture, extra_context={'titre':'Comptabilité: Factures'}), name='factures'),
    path('facture_detail/<int:pk>', views.detailFacture,name='facture_detail'),

    #path('facture_detail/<int:pk>', DetailView.as_view(model=Facture, extra_context={'factureSoldeForm':FactureSoldeForm, 'titre':'Detail facture'}), name='facture_detail'),
    #path('brouillon_detail/<int:pk>', DetailView.as_view(model=Brouillon, extra_context={'ligneForm':LigneForm(instance=Ligne(brouillon=Brouillon.objects.get(pk=182)))}), name='brouillon_detail'),
    path('brouillon_detail/<int:pk>', views.detailBrouillon, name='brouillon_detail'),
    path('facture_update/<int:pk>',UpdateView.as_view(model=Facture, fields='__all__'), name='update_facture'),
    path('deligne/', views.del_ligne_brouillon, name='deligne'),
    path('maj_ligne_brouillon/', views.maj_ligne_brouillon, name='maj_ligne_brouillon'),
    #path('maj_brouillon/', views.maj_brouillon, name='maj_brouillon'),
    path('addLigneBrouillon/', views.addLigneBrouillon, name='addLigneBrouillon'),
    path('addbrouillonNew/', views.addBrouillonNew, name='addbrouillonNew'),

    path('toto/',views.toto, name='toto'),
    #path('test/delete/<int:pk>', views.del_ligne_brouillon_bis, name="test_delete"),
    path('add_line_test/', views.add_line_test, name='add_line_test'),
    path('editLigne/<int:pk>', views.maj_ligne_brouillon_test, name='editLigne'),
    # transfert en comptabilite




]
