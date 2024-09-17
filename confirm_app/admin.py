from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Empresa, Licenca, UserProfile

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nif', 'email', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('nome', 'nif', 'email')

@admin.register(Licenca)
class LicencaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'max_engagements', 'data_inicio', 'data_fim', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('empresa__nome',)
    date_hierarchy = 'data_inicio'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('empresa')
    
class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False
  verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
  inlines = (UserProfileInline,)
  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_empresa')

  def get_empresa(self, obj):
    try:
      return obj.userprofile.empresa
    except UserProfile.DoesNotExist:
      return None
  get_empresa.short_description = 'Empresa'
  get_empresa.admin_order_field = 'userprofile__empresa'

# Re-registre o UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registre o modelo Empresa se ainda não estiver registrado
# admin.site.register(Empresa)