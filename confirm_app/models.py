from django.db import models
import uuid

class Engagement(models.Model):
    cliente = models.CharField(max_length=50)
    referencia = models.CharField(max_length=50)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("Engagement_detail", kwargs={"pk": self.pk})

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
   

    def __str__(self):
        return self.terceiro
