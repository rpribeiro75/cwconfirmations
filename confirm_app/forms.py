from django import forms
from .models import Cliente, PedidoTerceiros, Engagement


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nome', 'cliente_codigo']
        
    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.empresa:
            instance.empresa = self.empresa
        if commit:
            instance.save()
        return instance

class EngagementForm(forms.ModelForm):
  class Meta:
      model = Engagement
      fields = ["cliente", "engagement_nome", 'engagement_referencia', "pdf_assinado"]
      
  def __init__(self, *args, **kwargs):
      empresa = kwargs.pop('empresa', None)
      super().__init__(*args, **kwargs)
      if empresa:
          self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)
          self.fields['cliente'].widget.attrs['readonly'] = True
          self.fields['cliente'].widget.attrs['disabled'] = True

  def clean_cliente(self):
      # Garante que o cliente não seja alterado no formulário
      return self.initial.get('cliente')

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
        widgets = {
            'saldo_resposta_cliente' : forms.TextInput(attrs={'type':'number','class':'form-control form-input','placeholder':'Insira aqui o saldo'}),
            'anexo_resposta_cliente' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
            'saldo_resposta_cliente_titulos' : forms.TextInput(attrs={'type':'number','class':'form-control form-input'}),
            'anexo_resposta_cliente_titulos' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
            'saldo_resposta_fornecedor' : forms.TextInput(attrs={'type':'number','class':'form-control form-input'}),
            'anexo_resposta_fornecedor' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
            'saldo_resposta_fornecedor_titulos' : forms.TextInput(attrs={'type':'number','class':'form-control form-input'}),
            'anexo_resposta_fornecedor_titulos' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
            'saldo_resposta_odc' : forms.TextInput(attrs={'type':'number','class':'form-control form-input'}),
            'anexo_resposta_odc' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
            'saldo_resposta_outros' : forms.TextInput(attrs={'type':'number','class':'form-control form-input'}),
            'anexo_resposta_outros' : forms.TextInput(attrs={'type':'file','class':'form-control'}),
        }


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Selecione um arquivo CSV')



class SaldoUpdateForm(forms.Form):
    saldo = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, required=True)
    anexo_resposta_cliente = forms.FileField(label='Anexar extrato', required=False)

