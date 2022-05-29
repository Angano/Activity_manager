from django.forms import ModelForm
from .models import Activite
from django.forms import TextInput, Textarea, NumberInput


class ActiviteForm(ModelForm):
    class Meta:
        model = Activite
        fields = '__all__'
        #exclude = ('authorized','composition')
        widgets = {
            'nom': TextInput(attrs={'class':'form-control','placeholder':'Nom'}),
            'prix': NumberInput(attrs={'class':'form-control', 'style':'width:5rem'}),
            'description': Textarea(attrs={'class':'form-control','cols':20, 'rows':3})
        }