from django.db import models
from django.db.models import Max
from django.utils import timezone

from famille.models import Parent
from activite.models import Activite



# Create your models here.


class Brouillon(models.Model):
    date_brouillon = models.DateField(default=timezone.localdate())
    num_piece = models.IntegerField(unique=True, default='1')
    client = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='client_factured')
    factured = models.BooleanField(default=False)
    total = models.FloatField(default=0)


class Facture(models.Model):
    date_facture = models.DateField(default=timezone.now)
    num_piece = models.IntegerField(unique=True, default='1')
    client = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='client')
    total = models.FloatField(default=0)
    brouillon_origin = models.OneToOneField(Brouillon, on_delete=models.CASCADE )
    solder = models.BooleanField(default=False)
    note = models.TextField(max_length=250, default='', blank=True, null=True)
    date_solde = models.DateField(default=None, blank=True, null=True)

    def transfered_brouillon(self, brouillons):
        for brouillon in brouillons:
            dat = Brouillon.objects.get(pk=brouillon)
            #on recupre le dernier numéro de facture fc

            num_facture = Facture.objects.aggregate(Max('num_piece'))

            if num_facture['num_piece__max'] == None:
                num_facture=1
            else:
                num_facture = int(num_facture['num_piece__max'])+1
            #on copie les lignes du brouillon vers la facture
            facture = Facture(num_piece=num_facture, client=dat.client, total=dat.total, brouillon_origin=dat,date_facture=dat.date_brouillon)
            facture.save()

            dat.factured=True
            dat.save()

        # on attribue factured = true à brouillon



class Ligne(models.Model):

    article = models.ForeignKey(Activite , on_delete=models.CASCADE, default='')
    description = models.TextField(max_length=250, default='', blank=True, null=True)
    prix = models.FloatField(default=0, blank=True, null=True)
    quantite = models.FloatField(default=0, blank=True, null=True)
    total = models.FloatField(default=0, blank=True, null=True)
    brouillon = models.ForeignKey(Brouillon, on_delete=models.CASCADE, default='', blank=True, null=True, related_name='brouillon' )
    comptabilised = models.BooleanField(default=False)




