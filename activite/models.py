
from famille.models import Enfant
from user.models import Role
from django.db import models
from django.contrib.auth.models import User

class Activite(models.Model):
    nom = models.CharField(max_length=50)
    prix = models.FloatField(default=0.00)
    composition = models.ManyToManyField(Enfant, blank=True)
    authorized = models.ManyToManyField(User, blank=True,default='')
    description = models.TextField(default='', blank=True, null=True)

