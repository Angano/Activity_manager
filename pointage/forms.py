from django.forms import ModelForm
from .models import Pointage
from django.forms import HiddenInput, TextInput

class PointageForm(ModelForm):
    class Meta:
        model = Pointage
        fields = ['datepointage','activite','releve']
        widgets = {
            'activite':HiddenInput(),
            'datepointage':TextInput(attrs={'class': 'tuiu '})
        }

