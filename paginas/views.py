import datetime

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Chave, Paridades
from rest_framework.decorators import api_view
from .serializers import ParidadesSerializer, ChaveSerializer
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return render(request, 'paginas/home.html')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'paginas/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    username = request.POST.get('username')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    chave = request.POST.get('chave')

    if not nome or not sobrenome or not email or not senha \
            or not senha2 or not chave:
        messages.add_message(request, messages.WARNING, 'Nenhum campo pode estar vazio.')
        return render(request, 'paginas/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'E-mail invalido.')
        return render(request, 'paginas/cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.WARNING, 'A senha precisa ter 8 caracteres ou mais')
        return render(request, 'paginas/cadastro.html')
    if len(username) < 6:
        messages.add_message(request, messages.WARNING, 'O nome de usuario precisa ter 6 caracteres ou mais')
        return render(request, 'paginas/cadastro.html')
    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'As senhas são diferentes.')
        return render(request, 'paginas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Já temos um usuario cadastrado com esse e-mail')
        return render(request, 'paginas/cadastro.html')

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'Nome de usuario indisponível')
        return render(request, 'paginas/cadastro.html')

    if not Chave.objects.filter(chave=chave).exists():
        messages.add_message(request, messages.INFO, 'Chave inexistente')
        return render(request, 'paginas/cadastro.html')
    else:
        usuarios = User.objects.all()
        for usuario in usuarios:
            if Chave.objects.filter(chave=chave, usuario=usuario).exists() and usuario != None:
                messages.add_message(request, messages.INFO, f'Outro usuario já Cadastrou essa chave')
                return render(request, 'paginas/cadastro.html')

    key = Chave.objects.get(chave=chave)

    user = User.objects.create_user(username=username, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)

    id_usuario = User.objects.get(username=username)
    ativacao = timezone.now()
    expiracao = ativacao + timedelta(days=30)
    creat_chave = Chave(
        id=key.id,
        usuario=id_usuario,
        chave=chave,
        data_criacao=ativacao,
        data_expiracao=expiracao,
    )

    creat_chave.save()
    user.save()
    messages.add_message(request, messages.SUCCESS, f'Cadastro criado com sucesso, agora entre em sua conta')
    return redirect('entrar')


def entrar(request):
    if request.method != "POST":
        return render(request, 'paginas/entrar.html')

    usuario = request.POST.get('username')
    senha = request.POST.get('senha')
    try:
        ver_usuario = User.objects.get(username=usuario)
    except:
        messages.add_message(request, messages.ERROR, 'Credenciais inválidas')
        messages.add_message(request, messages.WARNING, 'Tanto o usuario como a senha diferencia letras minusculas de maiusculas')
        return render(request, 'paginas/entrar.html')

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
        if not ver_usuario.is_active:
            messages.add_message(request, messages.ERROR, 'Chave expirada! contate o suporte')
            return render(request, 'paginas/entrar.html')
        messages.add_message(request, messages.ERROR, 'Credenciais inválidas')
        messages.add_message(request, messages.WARNING, 'Tanto o usuario como a senha diferencia letras minusculas de maiusculas')
        return render(request, 'paginas/entrar.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Bem vindo! {usuario}')
        return redirect('perfil')


@login_required(redirect_field_name='login')
def perfil(request):
    return render(request, 'paginas/perfil.html')


@login_required(redirect_field_name='login')
def sair(request):
    auth.logout(request)
    return redirect('entrar')


@login_required(redirect_field_name='login')
def download(request):
    return render(request, 'paginas/download.html')


@api_view(['POST'])
def paridades_list(request):
    if request.method == "POST":
        post = request.data
        try:
            usuario = post['username']
            user = User.objects.get(username=usuario)
            if not user.is_active:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                if post['paridade']:
                    paridades = Paridades.objects.all()
                    if user.is_superuser and post['paridade'] == "todas":
                        serializer = ParidadesSerializer(paridades, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        for paridade in paridades:
                            if paridade.paridade == post['paridade']:
                                par = Paridades.objects.get(paridade=post['paridade'])
                                serializer = ParidadesSerializer(par)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def atualizar_paridade(request):
    if request.method == "POST":
        post = request.data     # pegando as informações
        try:    # Verificando e separando as informações
            paridade = post["paridade"]
            call = post["call"]
            put = post["put"]
            usuario = post['username']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=usuario)
        if not user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            paridades = Paridades.objects.all()
            for c in paridades:
                if c.paridade == paridade:
                    par = Paridades.objects.get(paridade=paridade)
                    atualizacao = Paridades(
                        id=par.id,
                        paridade=paridade,
                        call=call,
                        put=put
                    )
                    atualizacao.save()
                    return Response(status=status.HTTP_200_OK)
                
            new = Paridades(
                paridade=paridade,
                call=call,
                put=put
            )
            new.save()
            return Response(status=status.HTTP_201_CREATED)
        

@api_view(["POST"])
def verificar_usuarios(request):
    if request.method == "POST":
        post = request.data
        try:
            usuario = post['username']
            n_user = User.objects.get(username=usuario)
            if not n_user.is_active:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            senha = post['senha']
            
            user = auth.authenticate(request, username=usuario, password=senha)
            if not user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bloquear_user(request):
    now = timezone.now()
    if request.method == "GET":
        chaves = Chave.objects.all()
        for chave in chaves:
            if chave.data_expiracao <= now:
                user = User.objects.get(username=chave.usuario.username)
                desativar = User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_active=False
                )
                desativar.save()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def criar_chave(request):
    if request.method == "POST":
        post = request.data
        try:
            chave = post["chave"]
            usuario = post['username']
            senha = post['senha']
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = auth.authenticate(request, username=usuario, password=senha)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if user.is_superuser:
                chaves = Chave.objects.all()
                for key in chaves:
                    if key.chave == chave:
                        return Response(status=status.HTTP_304_NOT_MODIFIED)
                new = Chave(
                    chave=chave,
                    usuario=None,
                )
                new.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def verificar_chave(request):
    if request.method == "POST":
        post = request.data
        try:
            usuario = post['username']
            senha = post['senha']
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = auth.authenticate(request, username=usuario, password=senha)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if user.is_superuser:
                livres = []
                chaves = Chave.objects.all()
                for chave in chaves:
                    if not chave.usuario:
                        livres.append(chave)
                serializer = ChaveSerializer(livres, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
