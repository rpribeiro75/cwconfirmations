from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['saldo', 'arquivo']


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV')



class SaldoUpdateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, required=True)
    arquivo = forms.FileField(label='Anexar arquivo', required=False)

