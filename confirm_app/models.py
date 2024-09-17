from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
import uuid

class Empresa(models.Model):
  nome = models.CharField(max_length=200)
  nif = models.CharField(max_length=14, unique=True)
  endereco = models.TextField()
  telefone = models.CharField(max_length=20)
  email = models.EmailField()
  data_criacao = models.DateTimeField(auto_now_add=True)
  ativa = models.BooleanField(default=True)

  # Relação com o usuário (assumindo que um usuário pode estar associado a uma empresa)
  usuario_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresa_admin')

  def __str__(self):
      return self.nome

  @property
  def licenca_atual(self):
      try:
          return self.licenca
      except Licenca.DoesNotExist:
          return None

  def pode_criar_engagement(self):
      licenca = self.licenca_atual
      if not licenca or not licenca.is_valid():
          return False
      return licenca.engagements_disponiveis() > 0

  def total_engagements(self):
      return self.engagement_set.count()

  def engagements_ativos(self):
      return self.engagement_set.filter(status='ativo').count()

  def dias_ate_expiracao_licenca(self):
      licenca = self.licenca_atual
      if licenca and licenca.is_valid():
          return (licenca.data_fim - timezone.now().date()).days
      return 0

class Licenca(models.Model):
  empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='licencas')
  max_engagements = models.PositiveIntegerField()
  data_inicio = models.DateField()
  data_fim = models.DateField()
  ativa = models.BooleanField(default=True)

  def clean(self):
      if self.data_fim <= self.data_inicio:
          raise ValidationError("A data de fim deve ser posterior à data de início.")
      
      # Verifica se há sobreposição com outras licenças ativas
      sobreposicao = Licenca.objects.filter(
          empresa=self.empresa,
          ativa=True,
          data_inicio__lte=self.data_fim,
          data_fim__gte=self.data_inicio
      ).exclude(pk=self.pk)
      
      if sobreposicao.exists():
          raise ValidationError("Existe sobreposição com outra licença ativa.")

  def save(self, *args, **kwargs):
      self.full_clean()
      super().save(*args, **kwargs)

  def is_valid(self):
      hoje = timezone.now().date()
      return self.ativa and self.data_inicio <= hoje <= self.data_fim

  def engagements_disponiveis(self):
      return self.max_engagements - self.empresa.engagements.filter(
          data_criacao__gte=self.data_inicio,
          data_criacao__lte=self.data_fim
      ).count()
  

class Cliente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
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
    data_criacao = models.DateField(auto_now_add=True)
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ativo', 'Ativo'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado')
    ], default='ativo')
    pdf_assinado = models.FileField(upload_to='pdfs_assinados/', blank=True, null=True)

    def __str__(self):
        return self.engagement_nome

    def get_absolute_url(self):
        return reverse("engagement_list")
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Novo engagement
            if not self.cliente.empresa.pode_criar_engagement():
                raise ValidationError("Limite de engagements atingido ou licença inválida.")
        super().save(*args, **kwargs)

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
    
    link_unico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    primeiro_envio = models.DateTimeField(null=True, blank=True)
    ultimo_envio = models.DateTimeField(null=True, blank=True)
    respondido = models.DateTimeField(null=True, blank=True)

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
    anexo_resposta_cliente = models.FileField(upload_to='arquivos/', blank=True)
    anexo_resposta_cliente_titulos = models.FileField(upload_to='arquivos/', blank=True)
    anexo_resposta_fornecedor = models.FileField(upload_to='arquivos/', blank=True)
    anexo_resposta_fornecedor_titulos = models.FileField(upload_to='arquivos/', blank=True)
    anexo_resposta_odc = models.FileField(upload_to='arquivos/', blank=True)
    anexo_resposta_outros = models.FileField(upload_to='arquivos/', blank=True)
    movsctb_cliente = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsctb_cliente_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsctb_fornecedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsctb_fornecedor_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsctb_odc = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsctb_outros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_cliente = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_cliente_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_fornecedor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_fornecedor_titulos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_odc = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    movsterceiro_outros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    conciliado_cliente = models.BooleanField(default=False)
    conciliado_cliente_titulos = models.BooleanField(default=False)
    conciliado_fornecedor = models.BooleanField(default=False)
    conciliado_fornecedor_titulos = models.BooleanField(default=False)
    conciliado_odc = models.BooleanField(default=False)
    conciliado_outros = models.BooleanField(default=False)
   

    def __str__(self):
        return self.terceiro


class EmpresaFilterMixin:
  def get_queryset(self):
      return super().get_queryset().filter(empresa=self.request.user.empresa)
