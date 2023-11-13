from django import forms
from .models import Cliente, PedidoTerceiros, Engagement


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nome', 'cliente_codigo']

class EngagementForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ["engagement_nome",'engagement_referencia']

class PedidoTerceirosForm(forms.ModelForm):
    class Meta:
        model = PedidoTerceiros
        fields = ['saldo', 'anexo']


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV')



class SaldoUpdateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, required=True)
    anexo = forms.FileField(label='Anexar extrato', required=False)

