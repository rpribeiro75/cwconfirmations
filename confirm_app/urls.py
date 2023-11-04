from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('criar_engagement', views.criar_engagement, name="criar_engagement"),
    path('importar-csv/', views.ImportarCSV.as_view(), name='importar_csv'),
    path('visualizar/', views.visualizar, name='visualizar'),
    path('pagina_saldo/<str:link_unico>/', views.PaginaSaldo.as_view(), name='pagina_saldo'),
    path('enviar_emails/', views.EnviarEmail.as_view(), name='enviar_emails'),
    path('pagina_sucesso/', views.PaginaSucesso.as_view(), name='pagina_sucesso'),
    path('editar-registro/<int:registro_id>/', views.editar_registro, name='editar_registro'),
    path('excluir-registro/<int:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('pagina_erro/', views.PaginaErro.as_view(), name='pagina_erro'),
   
  
]