from django.db import models
from django.db.models import Max

from django.utils import timezone

from activite.models import Activite
from famille.models import Enfant, Parent
from comptabilite.models import Ligne, Facture, Brouillon
from datetime import date
import datetime, calendar


class Pointage(models.Model):
    datepointage = models.DateField(blank=False, null=False)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE, null=True, blank=True, default='')
    releve = models.TextField(blank=True, null=True,default='')
    transfered = models.BooleanField(default=False)

    def data_releve(self):
        pointages = self.queryset
        dictionnaire = {}

        # creation du dictionnaire des activites
        activites = set([data.activite for data in pointages])

        # peuple avec les releve en fonction des activite

        for activite in activites:
            data_releve = []
            datas = pointages.filter(activite=activite)
            for data in datas:
                data_releve += (
                    data.releve.replace('[', "").replace(']', "").replace("'", '').replace(' ', '').split(','))

            # calcul total/élève sur l'activite
            total = dict()
            for item in data_releve:
                try:
                    eleve = item
                    if item in total:
                        total[eleve] = total[eleve] + 1
                    else:
                        total[eleve] = 1
                except:
                    print('hello')

            # Transformation du tableau=> remplacement index int par objet élève
            convert_dict = dict()
            for key, values in total.items():
                try:
                    toto = Enfant.objects.get(pk=key)
                    convert_dict[toto] = values
                except ValueError:
                    print('hello', key, ValueError)

            dictionnaire[activite] = convert_dict

        return dictionnaire

    def get_date(self):
        date_du_jour = datetime.datetime.now()
        date_range=calendar.monthrange(date_du_jour.year, date_du_jour.month)
        date_debut = date_du_jour.replace(day=1)
        date_fin = date_debut+datetime.timedelta(date_range[1]-1)
        data=(date_debut, date_fin)

        return data

    def data_releve2(self, valid_brouillon=False, liste_activite=None, date_debut=None, date_fin=None):

        if date_debut == None:
            date_debut = self.get_date()[0].strftime('%Y-%m-%d')
        if date_fin == None:
            date_fin = self.get_date()[1].strftime('%Y-%m-%d')
        if liste_activite != None and valid_brouillon=='1':
            pointages = Pointage.objects.filter(transfered=False, activite__in=liste_activite, datepointage__range=(date_debut, date_fin))
        else:
            pointages = Pointage.objects.filter(transfered=False, datepointage__range=(date_debut, date_fin))

        dictionnaire = {}

         # creation d'un dictionnaire des activites
        activites = set([data.activite for data in pointages])

        # peuple avec les relevés en fonction des activités
        for activite in activites:

            data_releve = []
            datas = pointages.filter(activite=activite)

            for data in datas:
                if valid_brouillon:
                    data.transfered=True
                    data.save()

                data_releve+=(data.releve.replace('[', '').replace(']', '').replace('"', '').replace(' ', '').split(','))

            # on supprime les pointages vides
            data_releve = [x for x in data_releve if x]

            # calcul total/élève sur l'activite
            total = dict()

            # Calcul du nombre de pointages par activité
            for item in data_releve:
                if item:
                    try:
                        eleve = item
                        if item in total:
                            total[eleve] = total[eleve] + 1
                        else:
                            total[eleve] = 1
                    except:
                        print('hello')

            # Transformation du tableau=> remplacement index int par objet élève
            convert_dict = dict()

            for key, values in total.items():
                try:
                    toto = Enfant.objects.get(pk=key)
                    convert_dict[toto] = values


                except ValueError:
                    print('error', key, ValueError)


            # liste des activités pointées au format activité, élèves, nbre pointages, montant total
            if len(data_releve)>0:
                dictionnaire[activite] = [convert_dict,len(data_releve),len(data_releve)*activite.prix]
        print(dictionnaire)
        if valid_brouillon == '1':

            for key, value in dictionnaire.items():
                total_ligne = 0
                for eleve, quantite in value[0].items():
                    total_ligne = int(quantite)*float(key.prix)
                    num_piece = Brouillon.objects.aggregate(Max('num_piece'))
                    if num_piece['num_piece__max'] == None:
                        num_piece = 1
                    else:
                        num_piece = int(num_piece['num_piece__max'])+1
                    piece, created = Brouillon.objects.filter(factured=False).get_or_create(client=eleve.parent1, defaults={'num_piece':num_piece})
                    datat = Brouillon.objects.get(pk=piece.pk)
                    datat.total+=total_ligne
                    datat.save()
                    ligne = Ligne(article=key, prix=float(key.prix), quantite=int(quantite), total=total_ligne, brouillon=piece, description=eleve.prenom, comptabilised=True)
                    ligne.save()


                                                                
        return dictionnaire
        
        #return data

