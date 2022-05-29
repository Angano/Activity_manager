from django.shortcuts import render
from .forms import PointageForm
from .models import Activite, Pointage, Enfant
from django.forms import HiddenInput
import json
from datetime import datetime, date
from django.http import HttpResponse


# Create your views here.
def pointage(request):
    user_activite = set(Activite.objects.filter(authorized__pk=request.user.pk))

    return render(request,'pointage/pointage.html', {'activites':user_activite})

def detail(request):
    if False:
        pointage = Pointage.objects.get(pk=4)

        pointageform = PointageForm(instance=pointage, initial={'pointage':pointage.pointage})

        if request.method == 'POST':
            titi=(request.POST.getlist('toto'))
            pointageform = PointageForm(request.POST, instance=pointage)
            if pointageform.is_valid():
                data = pointageform.save(commit=False)
                data.pointage = titi
                data.save()
                pointageform = PointageForm(instance=Pointage.objects.get(pk=4))
            else:
                print(pointageform.errors)

        pointageform.fields['activite'].widget = HiddenInput()
        return render(request,'pointage/detail.html',{'pointage':pointage,'pointageform':pointageform})
    else:
        return HttpResponse('suis perdu')

def add_pointage(request,pk):

    if request.is_ajax():
        datepointage=datetime.strptime(request.POST.get('datepointage'), "%Y-%m-%d").strftime("%Y-%m-%d")

        try:
            pointage = Pointage.objects.get(activite=Activite.objects.get(pk=pk), datepointage=datepointage)
            donnee = pointage.releve
            transfered = pointage.transfered


            if len(donnee)==0:
                donnee = json.dumps([])
                transfered = False
        except Pointage.DoesNotExist:
            donnee = json.dumps([])
            transfered = False
        data = dict()
        data['transfered'] = transfered
        data['donnee']= donnee

        return HttpResponse(json.dumps(data))

    if request.method == 'POST':
        pointage, created = Pointage.objects.get_or_create(activite=Activite.objects.get(pk=pk),
                                                           datepointage=datetime.strptime(request.POST.get('datepointage'), "%Y-%m-%d").strftime("%Y-%m-%d"))
        pointageform = PointageForm(request.POST,instance=pointage)
        if pointageform.is_valid():
            pointage = pointageform.save(commit=False)
            releve = json.dumps(list(request.POST.getlist('releve')))
            pointage.releve = releve
            pointage.save()
        else:
            print(pointageform.errors)
    else:
        pointage, created = Pointage.objects.get_or_create(activite=Activite.objects.get(pk=pk),
                                                           datepointage=date.today())
        pointageform = PointageForm(instance=pointage)
    try:
        releve = [int(data) for data in list(json.loads(pointage.releve))]
    except:
        releve = list()

    return render(request, 'pointage/add_pointage.html',{'pointageform':pointageform,'pointage':pointage, 'releve':releve})

def synthese_mensuelle(request, pk, datepointage=datetime.now().strftime("%Y-%m")):
    if request.method =='POST':
        if request.is_ajax():
            datepointage = (request.POST.get('datepointage'))
            pk=int(request.POST.get('pk'))
    pointages = Pointage.objects.filter(activite=pk, datepointage__contains=datepointage).order_by('datepointage')
    activite = Activite.objects.get(pk=pk)
    eleves = Activite.objects.get(pk=pk).composition.all()

    return render(request, 'pointage/synthese_mensuelle.html',{'activite':activite, 'pointages':pointages, 'eleves':eleves})

# Requète ajax pour obtenir l'activite et le pointage associé
def getPointage(request,pk):
    pointage, created = Pointage.objects.get_or_create(activite=Activite.objects.get(pk=pk), datepointage=date.today())
    pointageform = PointageForm(instance=pointage)

    try:
        releve = [int(data) for data in list(json.loads(pointage.releve))]
    except:
        releve = list()

    return render(request, 'pointage/add_pointage.html',    {'pointageform': pointageform, 'pointage': pointage, 'releve': releve})
