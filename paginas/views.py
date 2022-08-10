from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Chave


def home(request):
    pass


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
        messages.add_message(request, messages.WARNING, 'a senha precisa ter 8 caracteres ou mais')
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

    if Chave.objects.filter(chave=chave).exists():
        usuarios = User.objects.all()
        for usuario in usuarios:
            if Chave.objects.filter(usuario=usuario).exists():
                messages.add_message(request, messages.INFO, 'Chave inexistente')
                return render(request, 'paginas/cadastro.html')

    messages.add_message(request, messages.SUCCESS, 'Registrado com sucesso. Agora entre na sua conta')
    user = User.objects.create_user(username=username, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
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