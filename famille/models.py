from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Parent(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15, default='')
    email = models.EmailField( default='')
    adresse = models.CharField(max_length=100, default='')
    code_postal = models.CharField(max_length=8, default='')
    ville = models.CharField(max_length=100, default='')

    def get_absolute_url(self):
        return reverse('famille:parents')

    def enfants(self):
        return self.parent1.all()

class Enfant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    parent1 = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent1', default='')
    parent2 = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent2', default='')


