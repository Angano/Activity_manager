from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .forms import ParentForm, EnfantForm
from .models import Enfant, Parent
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import UpdateView

from django.core import serializers

# Create your views here.

@login_required
def parent(request):
    form = ParentForm()
    if request.is_ajax():
        if request.method == 'POST':
            parents = Parent.objects.filter(nom__contains=request.POST.get('parent'))
            liste_parent = ""
            for parent in parents:
                liste_parent += '<span class="btn btn-light btn-sm d-block w-100" id="parent_'+str(parent.pk)+'">'+parent.nom+' '+parent.prenom+'</span>'
            liste_parent += ""
            return HttpResponse(liste_parent)
        else:
            return HttpResponse('oups')
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, 'famille/add_parent.html', {'form':form})

@login_required
def enfant(request):
    form = EnfantForm()
    if request.method == 'POST':
        form = EnfantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/famille/enfants/')
        else:
            print(form.errors)
    return render(request, 'famille/enfant.html', {'form':form})

def famille(request):
    form = FamilleForm()
    if request.method == 'POST':
        form = FamilleForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, 'famille/famille.html',{'form':form})

def userDetail(request,pk):
    enfant = Enfant.objects.get(pk=pk)
    fratrie =  Enfant.objects.filter(Q(parent1=enfant.parent1) | Q(parent2=enfant.parent2)).distinct()

    return render(request, 'famille/enfant_detail.html',{'enfant':enfant, 'fratrie':fratrie, 'titre':'Detail d\'un enfants'})

# requet ajax
def add_enfant_ajax(request):
    if request.method == 'POST':
        eleves = Enfant.objects.filter(Q(nom__contains=request.POST.get('eleve'))| Q(prenom__contains=request.POST.get('eleve')))
        liste_eleve = "<ul>"
        for eleve in eleves:
            liste_eleve+="<li>"+eleve.nom+" "+eleve.prenom+", "+eleve.parent1.nom+" "+eleve.parent1.prenom+", "+eleve.parent2.nom+" "+eleve.parent2.prenom+"</li>"
        liste_eleve+= '</ul>'

    return HttpResponse(liste_eleve)

def searchParent(request):

    if request.method == 'POST':
        datas = Parent.objects.filter(nom__startswith=request.POST.get('parent'))
        return HttpResponse(serializers.serialize('json',datas))
    else:
        return HttpResponse('nothing')

# Update élève
class UpdateEleve(UpdateView):
    form_class=EnfantForm
    template_name='famille/enfant_form.html'
    queryset = Enfant.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context