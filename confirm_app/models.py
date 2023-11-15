from django.db import models
from django.urls import reverse
import uuid

class Cliente(models.Model):
    cliente_nome = models.CharField(max_length=50)
    cliente_codigo = models.IntegerField()

    def __str__(self):
        return self.cliente_nome

    def get_absolute_url(self):
        return reverse("cliente_list")



class Engagement(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    engagement_nome = models.CharField(max_length=50)
    engagement_referencia = models.CharField(max_length=50)
    pdf_assinado = models.FileField(upload_to='pdfs_assinados/', blank=True, null=True)

    def __str__(self):
        return self.engagement_nome

    def get_absolute_url(self):
        return reverse("engagement_list")

class PedidoTerceiros(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    terceiro = models.CharField(max_length=200)
    

    contacto = models.CharField(max_length=200)
    email = models.EmailField()

    conta_contabilidade_cliente = models.CharField(max_length=200)
    conta_contabilidade_cliente_titulos = models.CharField(max_length=200)
    conta_contabilidade_fornecedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    conta_contabilidade_fornecedor_titulos = models.CharField(max_length=200)
    conta_contabilidade_odc = models.CharField(max_length=200)
    conta_contabilidade_outros = models.CharField(max_length=200)

    saldo_contabilidade_cliente = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_contabilidade_cliente_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_contabilidade_fornecedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_contabilidade_fornecedor_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_contabilidade_odc = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_contabilidade_outros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_cliente = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_cliente_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_fornecedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_fornecedor_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_odc = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    saldo_resposta_outros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    anexo = models.FileField(upload_to='arquivos/', blank=True)
    link_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    primeiro_envio = models.DateTimeField(null=True, blank=True)
    ultimo_envio = models.DateTimeField(null=True, blank=True)
    respondido = models.DateTimeField(null=True, blank=True)
    conciliado = models.BooleanField(default=False)

   

    def __str__(self):
        return self.terceiro

