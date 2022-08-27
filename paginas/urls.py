from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('entrar/', views.entrar, name='entrar'),
    path('accounts/login/', views.entrar, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('download/', views.download, name='download'),
    path('sair/', views.sair, name='sair'),
    path('api/paridade/', views.paridades_list, name='paridades_list'),
    path('api/paridade/criar', views.criar_paridade, name='criar_paridade'),
    path('api/paridade/atualizar', views.atualizar_paridade, name='atualizar_paridade'),
    path('api/usuarios/verificar', views.verificar_usuarios, name='user'),
    path('api/chaves/criar', views.criar_chave, name='criar_chave'),
    path('api/chaves/verificar', views.verificar_chave, name='verificar_chave'),
]
