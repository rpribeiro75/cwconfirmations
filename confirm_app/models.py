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

    def __str__(self):
        return self.engagement_nome

    def get_absolute_url(self):
        return reverse("engagement_list")

class PedidoTerceiros(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    terceiro = models.CharField(max_length=200)
    conta_contabilidade = models.CharField(max_length=50)
    contacto = models.CharField(max_length=200)
    email = models.EmailField()
    saldo_contabilidade = models.CharField(max_length=50)
    saldo = models.TextField(blank=True)
    anexo = models.FileField(upload_to='arquivos/', blank=True)
    link_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    respondido = models.BooleanField(default=False)

   

    def __str__(self):
        return self.terceiro

