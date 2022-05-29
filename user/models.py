from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse

# Create your models here.

class Role(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('user:roles')


class Profil(models.Model):
    role = models.ManyToManyField(Role, blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE, default='')
    info = models.TextField(max_length=250, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('user:roles')



    def user_connected_roles(self):
        user_roles = [data.nom for data in self.role.all()]
        return user_roles
