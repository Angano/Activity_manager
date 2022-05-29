from django.forms import ModelForm, TextInput
from django.forms import HiddenInput
from .models import Parent, Enfant

class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
        widgets = {
            'nom':TextInput(attrs={'class':'form-control','placeholder':'Nom'}),
            'prenom': TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'adresse': TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'telephone': TextInput(attrs={'class': 'form-control', 'placeholder':'Téléphone'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'code_postal': TextInput(attrs={'class': 'form-control', 'placeholder': 'Code postal'}),
            'ville': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'})

                   }



class EnfantForm(ModelForm):
    class Meta:
        model = Enfant
        fields = '__all__'
        widgets = {
            'parent1':HiddenInput(),'parent2':HiddenInput(),
            'nom':TextInput(attrs={'class':'form-control'}),
            'prenom': TextInput(attrs={'class': 'form-control'}),
            }



