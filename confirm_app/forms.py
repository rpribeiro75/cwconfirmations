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
        fields = ['saldo_resposta_cliente', 'anexo_resposta_cliente',
                  'saldo_resposta_cliente_titulos', 'anexo_resposta_cliente_titulos',
                  'saldo_resposta_fornecedor', 'anexo_resposta_fornecedor',
                  'saldo_resposta_fornecedor_titulos', 'anexo_resposta_fornecedor_titulos',
                  'saldo_resposta_odc', 'anexo_resposta_odc',
                  'saldo_resposta_outros', 'anexo_resposta_outros',]


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV')



class SaldoUpdateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, required=True)
    anexo_resposta_cliente = forms.FileField(label='Anexar extrato', required=False)

