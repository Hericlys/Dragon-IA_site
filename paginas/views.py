from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Chave, Paridades
from rest_framework.decorators import api_view
from .serializers import ParidadesSerializer
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

    user = auth.authenticate(request, username=usuario, password=senha)
    if not user:
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


@api_view(['POST'])
def paridades_list(request):
    if request.method == "POST":
        post = request.data
        try:
            usuario = post['username']
            senha = post['senha']
            user = auth.authenticate(request, username=usuario, password=senha)
            if not user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                if post['paridade']:
                    paridades = Paridades.objects.all()
                    for paridade in paridades:
                        if paridade.paridade == post['paridade']:
                            par = Paridades.objects.get(paridade=post['paridade'])
                            serializer = ParidadesSerializer(par)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def atualizar_paridade(request):
    if request.method == "POST":
        post = request.data     # pegando as informações
        try:    # Verificando e separando as informações
            paridade = post["paridade"]
            payout = post["payout"]
            call = post["call"]
            put = post["put"]
            usuario = post['username']
            senha = post['senha']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = auth.authenticate(request, username=usuario, password=senha)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if user.is_superuser:
                paridades = Paridades.objects.all()
                for c in paridades:     # Verificando a paridade
                    if c.paridade == paridade:
                        par = Paridades.objects.get(paridade=paridade)
                        atualizacao = Paridades(
                            id=par.id,
                            paridade=paridade,
                            payout=payout,
                            call=call,
                            put=put
                        )
                        atualizacao.save()
                        return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)