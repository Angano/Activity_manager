from django.forms import ModelForm, CheckboxInput, HiddenInput

from django.contrib.auth.models import User
from .models import Profil, Role
from django.forms import TextInput, Textarea, EmailInput, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','last_name', 'first_name','email']
        widgets = {
            'username':TextInput(attrs={'class': 'form-control', 'placeholder':'Nom utilisateur'}),
            'last_name':TextInput(attrs={'class': 'form-control', 'placeholder':'Nom'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder':'Prénom'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder':'email'})
        }



class MenuModelChoiceField (ModelMultipleChoiceField):
    def label_from_instance (self, obj):
        return "%s"%(obj.nom)


class ProfilForm(ModelForm):

    role = MenuModelChoiceField(widget=CheckboxSelectMultiple(attrs={'class':'form-check-input'}),queryset=Role.objects.all())
    class Meta:
        model = Profil
        fields = '__all__'
        exclude =['user',]
        widgets = {
                'info':TextInput(attrs={'class': 'form-control', 'placeholder':'Info'}),
                   }



class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
                    'nom':TextInput(attrs={'class':'form-control','placeholder':'Nom'}),
                    'description': Textarea(attrs={'class': 'form-control', 'placeholder':'Description'}),
        }

