from django.contrib import admin
from .models import Empresa, Licenca

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