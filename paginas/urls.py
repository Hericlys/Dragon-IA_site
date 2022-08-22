from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('entrar/', views.entrar, name='entrar'),
    path('accounts/login/', views.entrar, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('sair/', views.sair, name='sair'),
    path('api/', views.paridades_list, name='paridades_list'),
    path('api/atualizar', views.atualizar_paridade, name='atualizar_paridade'),
    path('api/user', views.user, name='user'),
]
