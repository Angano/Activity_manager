from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from pointage.models import Pointage
from activite.models import Activite
from famille.models import Parent
from .models import Ligne, Brouillon, Facture
from django.db.models import Sum, Max
from .forms import LigneForm, BrouillonForm, FactureSoldeForm
from django.views.generic import DetailView
from django.db.models import Count, F, FloatField
import datetime, time

import json
# Create your views here.


def comptabilite(request):
    pointages = Pointage.objects.filter(transfered=False).values('activite__nom','activite__prix','activite').annotate(Count('activite'))
    brouillons = Brouillon.objects.filter(factured=False).order_by('date_brouillon')[:10]
    factures = Facture.objects.filter(solder=False).order_by('date_facture')[:10]
    relances = Facture.objects.filter(date_facture__lt=datetime.date.fromtimestamp(time.time()-30*24*60*60))
    return render(request, 'comptabilite/index.html',{'titre':'Comptabilité: Synthèse','relances':relances, 'pointages':pointages, 'brouillons':brouillons,'factures':factures})


def validation_pointage(request):
    date = [ date.strftime('%d-%m-%Y') for date in Pointage().get_date()]

    if request.method == "POST":

        date_debut = request.POST.get('date_debut').split('-')
        date_fin = request.POST.get('date_fin').split('-')

        date_debut = date_debut[2]+'-'+date_debut[1]+'-'+date_debut[0]
        date_fin = date_fin[2]+'-'+date_fin[1]+'-'+date_fin[0]
        if request.is_ajax():
            pointages = Pointage().data_releve2(False, None,date_debut, date_fin)
            return render(request, 'comptabilite/validation_pointage.html',{'pointages': pointages, 'titre': 'Comptabilité: Validation...'})
            #return HttpResponse(str(date_debut)+'-'+ str(date_fin))

        activites = request.POST.getlist('ligne')
        validation = request.POST.get('validation')
        Pointage().data_releve2(validation,activites,date_debut,date_fin)
        return HttpResponseRedirect('/comptabilite/validation_pointage')
    else:
        pointages = Pointage().data_releve2()
    print(pointages)
    return render(request, 'comptabilite/validation_pointage.html', {'pointages':pointages,'titre':'Comptabilité: Validation...', 'date':date})


def encaissement(request):
    return render(request, 'comptabilite/encaissement.html')

def relance(request):
    return render(request, 'comptabilite/relance.html')


def brouillons(request):
    brouillons = Brouillon.objects.filter(factured=False)
    if request.method =='POST':
        datas = request.POST.getlist('brouillons')
        facture = Facture()
        facture.transfered_brouillon(datas)
    return render(request, 'comptabilite/brouillons.html',{'brouillons':brouillons, 'titre':'Comptabilite: Brouillons'})

def del_ligne_brouillon(request):
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get('idligne')
        ligne = Ligne.objects.get(pk=pk)
        ligne.delete()
        total = Ligne.objects.filter(brouillon=ligne.brouillon).aggregate(som=Sum('total'))
        brouillon = Brouillon.objects.get(pk=ligne.brouillon.pk)
        brouillon.total=total['som']
        brouillon.save()

        return HttpResponse('hola')

def maj_ligne_brouillon(request):
    if request.method == 'POST':
        data = json.loads(request.POST.getlist('data')[0])
        prix = float(data['prix_uni'].replace(',','.'))
        quantite = float(data['quantite'].replace(',','.'))
        ligne = Ligne.objects.get(pk=data['id_ligne'])
        ligne.prix = prix
        ligne.quantite = quantite
        ligne.total = prix*quantite
        ligne.save()
        brouillon = Brouillon.objects.get(num_piece=ligne.brouillon.num_piece)
        total = Ligne.objects.filter(brouillon=brouillon).aggregate(Sum('total'))['total__sum']

        brouillon.total= total
        brouillon.save()



    return HttpResponse(data)

def addLigneBrouillon(request):

    if request.method == 'POST':
        ligneform = LigneForm(data=request.POST)

        if ligneform.is_valid():
            print(request.POST)
            ligne = ligneform.save(commit=False)
            ligne.total = float(ligne.prix)*float(ligne.quantite)
            ligne.save()

            brouillon = Brouillon.objects.get(pk=ligne.brouillon.pk)
            total = Ligne.objects.filter(brouillon=brouillon).aggregate(Sum('total'))['total__sum']
            brouillon.total=total
            brouillon.save()
            print("helo")
        else:
            print(ligneform.errors)
    return HttpResponse(request.POST)



def test(request):
    if request.method == 'POST':
        datas = [request.POST.getlist('add-nom'), request.POST.getlist('add-id-article'),
                request.POST.getlist('add-description'), request.POST.getlist('add-prix'),
                request.POST.getlist('add-quantite')]
        longueur = len(request.POST.getlist('add-nom'))

        il = 0
        date = request.POST.get('add_date').split('-')
        date = date[2] + '-' + date[1]+'-'+date[0]


        num_piece = Brouillon.objects.aggregate(Max('num_piece'))['num_piece__max']+1 # on récupère le num piece max
        Br = Brouillon( date_brouillon=date, factured=False, client=Parent.objects.get(pk=request.POST.get('pk_parent')), num_piece=num_piece)
        Br.save()

        totalFacture = 0
        while il<longueur:
            if datas[1][il] != '':
                totalLigne = float(datas[3][il])*float(datas[4][il])
                ligne = Ligne( article=Activite.objects.get(pk=datas[1][il]), description=datas[2][il],
                               prix=datas[3][il], quantite=datas[4][il], total = totalLigne, brouillon=Br, comptabilised=False)
                ligne.save()
                totalFacture += totalLigne
            il+=1
        Br.total = totalFacture
        Br.save()

        return HttpResponse( datas)
    else:
        return HttpResponse('bye')

def toto(request):
    form = LigneForm()
    return render(request, 'comptabilite/test.html', {'form':form})
"""
def del_ligne_brouillon_bis(request, pk):
    ligne = Ligne.objects.get(pk=pk)
    brouillon = ligne.brouillon
    ligne.delete()
    total = Ligne.objects.filter(brouillon=brouillon).aggregate(som=Sum('total'))
    brouillon.total=total['som']
    brouillon.save()

    lignes = Ligne.objects.filter(brouillon=brouillon)

    form = LigneForm(instance=ligne)
    return render(request, 'comptabilite/tata.html',{'brouillon':brouillon, 'ligneForm':form, 'lignes':lignes})
"""
def add_line_test(request):
    if request.method == 'POST':

        brouillon = Brouillon.objects.get(pk=request.POST.get('brouillon'))

        total = float(request.POST.get('prix'))*float(request.POST.get('quantite'))
        line = Ligne(total=total)
        ligne = LigneForm(data=request.POST, instance=line)

        if ligne.is_valid():


            ligne.save(commit=False)
            ligne.save()

            brouillon.total = Ligne.objects.filter(brouillon=line.brouillon).aggregate(Sum('total'))['total__sum']
            brouillon.save()
    return HttpResponse('holo')

def maj_ligne_brouillon_test(request, pk):


    ligne = Ligne.objects.get(pk=pk)
    brouillon = Brouillon.objects.get(pk=ligne.brouillon.pk)
    ligneForm = LigneForm(instance=ligne)
    if request.method == 'POST':
        form = LigneForm(request.POST, instance=ligne)
        if form.is_valid():

            form.save()

            total = Ligne.objects.filter(brouillon=ligne.brouillon.pk).aggregate(Sum('total'))['total__sum']
            brouillon.total=total
            brouillon.save()
    return render(request,'comptabilite/editLigne.html',{'form':form,'id_ligne':pk, 'brouillon':brouillon})



# nouveau brouillon bis
def addBrouillonNew(request):

    brouillonForm = BrouillonForm()
    ligneForm = LigneForm()
    if(request.method=='POST'):
        datasPost = dict(request.POST)

        longueur = len(datasPost['article'])

        compteur = 0
        try:
            num_piece = Brouillon.objects.aggregate(Max('num_piece'))['num_piece__max']+1 # on récupère le num piece max
        except Exception as e:

           num_piece=1
        brouillon = Brouillon(num_piece=num_piece)
        brouillonForm=BrouillonForm(data=request.POST, instance=brouillon)
        if (brouillonForm.is_valid()):
            test = brouillonForm.save(commit=False)
            test.save()
            # on boucle pour sauvegarder les lignes
            total = 0
            while compteur<longueur:
                ligne = {'article':datasPost['article'][compteur],
                         'description':datasPost['description'][compteur],
                         'prix':datasPost['prix'][compteur],
                         'quantite':datasPost['quantite'][compteur]}
                ligne2 = LigneForm(data=ligne)
                if ligne2.is_valid():
                    total+= float(datasPost['prix'][compteur])*float(datasPost['quantite'][compteur])
                    toto=ligne2.save(commit=False)
                    toto.brouillon=brouillon
                    toto.total=float(datasPost['prix'][compteur])*float(datasPost['quantite'][compteur])
                    toto.save()
                else:
                    print(ligne2.errors)

                compteur+=1
            test.total=total
            test.save()


        else:
            print(brouillonForm.errors)


    return render(request, 'comptabilite/addBrouillonNew.html',{'brouillonform':brouillonForm,'ligneform':ligneForm})


def detailBrouillon(request, pk):

    brouillon = Brouillon.objects.get(pk=pk)
    ligne = Ligne(brouillon=brouillon)
    ligneForm = LigneForm(instance=ligne)
    return render(request, 'comptabilite/brouillon_detail.html', {'object': brouillon, 'ligneForm':ligneForm})


# Detail Facture
def detailFacture(request, pk):
    facture = Facture.objects.get(pk=pk)
    form = FactureSoldeForm(instance=facture)
    if request.method == 'POST':
        form = FactureSoldeForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('comptabilite:factures')
        else:
            print(form.errors)
    return render(request, 'comptabilite/facture_detail.html',{'object':facture, 'form':form} )

# Edit Brouillon
class DetailBrouillon(DetailView):
    form_class = BrouillonForm
    template_name = 'comptabilite/brouillon_detailn.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


