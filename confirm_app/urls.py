from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cliente/', views.ClienteListView.as_view(), name='cliente_list'),
    path('cliente_criar/', views.ClienteCreateView.as_view(), name="cliente_criar"),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('engagement/', views.EngagementListView.as_view(), name='engagement_list'),
    path('engagement_criar/<int:cliente_pk>/', views.EngagementCreateView.as_view(), name="engagement_criar"),
    path('engagement/<int:pk>/editar', views.EngagementUpdateView.as_view(), name='engagement_update'),
    path('engagement/<int:pk>/', views.EngagementDetailView.as_view(), name='engagement_detail'),
    # path('engagement/<int:pk>/', views.EngagementDetailView.as_view(), name='engagement_detail'),^
    path('engagement/<int:pk>/importar_csv/', views.ImportarCSVParaEngagement.as_view(), name='importar_csv_engagement'),
    path('engagement/<int:pk>/criar_pedido_terceiro/', views.PedidoTerceirosCriar, name='criar_pedido_terceiro'),
 
  

    path('pagina_saldo/<str:link_unico>/', views.PaginaSaldo.as_view(), name='pagina_saldo'),
    path('enviar_emails_engagement/<int:engagement_id>/', views.EnviarEmailEngagement.as_view(), name='enviar_emails_engagement'),
    path('EnviarEmailRegistro/<int:registro_id>/', views.EnviarEmailRegistro.as_view(), name='enviar_email_registro'),
    # path('enviar_emails/', views.EnviarEmail.as_view(), name='enviar_emails'),
    path('pagina_sucesso/', views.PaginaSucesso.as_view(), name='pagina_sucesso'),
    path('editar-registro/<int:registro_id>/', views.editar_registro, name='editar_registro'),
    # path('excluir-registro/<int:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('pagina_erro/', views.PaginaErro.as_view(), name='pagina_erro'),
   
  
]