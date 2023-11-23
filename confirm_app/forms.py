from django import forms
from .models import Cliente, PedidoTerceiros, Engagement


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nome', 'cliente_codigo']

class EngagementForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ["engagement_nome",'engagement_referencia', "pdf_assinado"]

class CriarPedidoTerceirosForm(forms.ModelForm):
    class Meta:
        model = PedidoTerceiros
        fields = ['terceiro', 'conta_contabilidade_cliente', 'contacto', 'email', 'saldo_contabilidade_cliente']

class PedidoTerceirosForm(forms.ModelForm):
    class Meta:
        model = PedidoTerceiros
        fields = ["saldo_contabilidade_cliente",'saldo_resposta_cliente', 'anexo_resposta_cliente']


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV')



class SaldoUpdateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, required=True)
    anexo_resposta_cliente = forms.FileField(label='Anexar extrato', required=False)

