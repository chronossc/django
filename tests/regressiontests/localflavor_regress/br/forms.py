from django import forms
from models import BRCPFCNPJ

class BRCPFCNPJForm(forms.ModelForm):

    class Meta:
        model = BRCPFCNPJ
