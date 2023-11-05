from django.db import models
from django.urls import reverse
import uuid

class Engagement(models.Model):
    cliente = models.CharField(max_length=50)
    referencia = models.CharField(max_length=50)

    def __str__(self):
        return self.cliente

    def get_absolute_url(self):
        return reverse("engagement_list")

class Registro(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    terceiro = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    email = models.EmailField()
    saldo_contabilidade = models.CharField(max_length=50)
    saldo = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='arquivos/', blank=True)
    link_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    extrato = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)
   

    def __str__(self):
        return self.terceiro

class Autorizacao(models.Model):
    autorizador = models.CharField(max_length=200)
    email = models.EmailField()
    data_de_autorizacao = models.DateTimeField(auto_now_add=True)
    registros_autorizados = models.ManyToManyField('Registro', related_name='autorizacoes')
    ip_autorizador = models.GenericIPAddressField(blank=True, null=True)
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE)
    link_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    confirmado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Autorização de {self.autorizador}'