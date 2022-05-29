import sys
sys.path.append('/home/matthieu/Downloads/Activity_manager/activity_manager')
from django.http import HttpResponse
from django.shortcuts import redirect

from django.shortcuts import render
from .forms import ActiviteForm
from django.contrib.auth.models import User
from famille.models import Enfant
from user.models import Role, Profil
from django.core import serializers
from .models import Activite
import json

from django.core import serializers

# Create your views here.


def activite(request):
    return render(request,'activite/_activite.html')

def addActivite(request):
    form = ActiviteForm()
    enfants = Enfant.objects.all()
    authorizeds = Role.objects.all()
    tab =[]
    for data in enfants:
        tab.append(data.pk)
    activites = Activite.objects.all()
    eleves = Enfant.objects.all()
    if request.method == 'POST':
        form = ActiviteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/activite/list_activites')
        else:
            print(form.errors)
    #dataTab = json.dumps(tab)
    #item = Activite.objects.get(pk=1)
    #item.composition = dataTab
    #item.save()
    return render(request,'activite/addActivite.html',{'form':form, 'activites':activites, 'eleves':eleves,'tab':tab, 'authorizeds':authorizeds})

def editActivite(request, pk):
    enfants = Enfant.objects.all()
    activite = Activite.objects.get(pk=pk)
    activites = [data.pk for data in activite.authorized.all()]
    users = User.objects.filter(profil__role__nom='Agent')

    #roles = Role.objects.all()
    roles = Profil.objects.filter(role__nom='Agent')
    form = ActiviteForm(instance=activite)
    if request.method=='POST':
        form = ActiviteForm(request.POST, instance=activite)

        if form.is_valid():
            form.save()
            return redirect('/activite/list_activites/')
        else:
            print(form.errors)
    return render(request, 'activite/activite_detail.html', {'users':users, 'enfants':enfants,'activite':activite, 'form':form,'activites':activites, 'roles':roles, 'titre':'Edition d\'une activite'})


def test(request):
    return HttpResponse('hello')

def get_eleve(request):
    if request.method == 'POST':
        if request.is_ajax():
            data ='<ul>'
            data_eleve = list(request.POST.get('data_eleve').replace('[','').replace(']','').replace(',','').replace(' ',''))
            eleves = Enfant.objects.filter(nom__contains=request.POST.get('data')).exclude(pk__in=data_eleve)
            for eleve in eleves:
               data+='<li class="list-no_style " data-eleve="eleve" id="id_eleve_'+str(eleve.pk)+'">'+eleve.nom+' '+eleve.prenom+'</li>'
            data+='</ul>'

    return HttpResponse(data)


def articles(request):

    if request.method == 'POST':
        data = request.POST.get('datas')
        return HttpResponse(serializers.serialize('json', Activite.objects.filter(nom__startswith=data)))
    else:
        return HttpResponse({})