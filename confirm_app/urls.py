from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('criar_engagement/', views.EngagementCreateView.as_view(), name="criar_engagement"),
    path('engagement/', views.EngagementListView.as_view(), name='engagement_list'),
    path('engagement/<int:pk>/editar', views.EngagementUpdateView.as_view(), name='engagement_update'),
    path('engagement/<int:pk>/', views.EngagementDetailView.as_view(), name='engagement_detail'),
    # path('engagement/<int:pk>/', views.EngagementDetailView.as_view(), name='engagement_detail'),^
    path('engagement/<int:pk>/importar_csv/', views.ImportarCSVParaEngagement.as_view(), name='importar_csv_engagement'),
    path('engagement/<int:pk>/autorizar/', views.autorizar, name='autorizar_engagement'),
    path('engagement/<int:pk>/confirmar-autorizacao/<str:link_unico>/', views.confirmar_autorizacao, name='confirmar_autorizacao'),
    # path('importar-csv/', views.ImportarCSV.as_view(), name='importar_csv'),
    path('visualizar/', views.visualizar, name='visualizar'),
    path('pagina_saldo/<str:link_unico>/', views.PaginaSaldo.as_view(), name='pagina_saldo'),
    path('enviar_emails_engagement/<int:engagement_id>/', views.EnviarEmailEngagement.as_view(), name='enviar_emails_engagement'),
    path('EnviarEmailRegistro/<int:registro_id>/', views.EnviarEmailRegistro.as_view(), name='enviar_email_registro'),
    # path('enviar_emails/', views.EnviarEmail.as_view(), name='enviar_emails'),
    path('pagina_sucesso/', views.PaginaSucesso.as_view(), name='pagina_sucesso'),
    path('editar-registro/<int:registro_id>/', views.editar_registro, name='editar_registro'),
    path('excluir-registro/<int:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('pagina_erro/', views.PaginaErro.as_view(), name='pagina_erro'),
   
  
]