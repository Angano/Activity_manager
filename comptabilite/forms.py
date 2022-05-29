from django.forms import ModelForm
from comptabilite.models import Facture, Ligne, Brouillon
from django.forms import HiddenInput, TextInput, NumberInput, CheckboxInput

class FactureForm(ModelForm):
    class Meta:
        model = Facture
        fields = ['client','date_facture']

class LigneForm(ModelForm):
    class Meta:
        model = Ligne
        fields = '__all__'

        widgets = {
            'brouillon': HiddenInput(),
            'article': HiddenInput(),
            'comptabilised':HiddenInput(),
            'description': TextInput(attrs={'class': 'form-control editable','placeholder':'Description'}),
            'prix': NumberInput(attrs={'class': 'form-control calcul  editable','placeholder':'Prix'}),
            'quantite': NumberInput(attrs={'class': 'form-control calcul editable','placeholder':'Quantité'}),
            'total': NumberInput(attrs={'class': 'form-control total','disabled':True,'placeholder':'Total'}),

        }

class BrouillonForm(ModelForm):
    class Meta:
        model = Brouillon
        fields = ['client','date_brouillon']
        widgets = {
                        'total': TextInput(attrs={'class': 'form-control total d-inline w-50','disabled':True,'placeholder':'Total'}),
                        'date_brouillon':TextInput(attrs={'class': 'form-control'})

        }

class FactureSoldeForm(ModelForm):
        class Meta:
            model = Facture
            fields = ['note','solder', 'date_solde']
            widgets = {
                'solder': CheckboxInput(attrs={'class': 'form-control form-check-input'}),
                'note':TextInput(attrs={'class': 'form-control'}),
                'date_solde': TextInput(attrs={'class': 'form-control', 'required':True})

            }