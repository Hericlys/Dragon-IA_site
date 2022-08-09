from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'paginas/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    username = nome + '_' + sobrenome
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    chave = request.POST.get('chave')

    if not nome or not sobrenome or not email or not senha \
            or not senha2 or not chave:
        messages.add_message(request, messages.ERROR, 'Nenhum campo pode estar vazio.')
        return render(request, 'paginas/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'E-mail invalido.')
        return render(request, 'paginas/cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'a senha precisa ter 8 caracteres ou mais')
        return render(request, 'paginas/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'As senhas são diferentes.')
        return render(request, 'paginas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, 'Já temos um usuario cadastrado com esse e-mail')
        return render(request, 'paginas/cadastro.html')

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'Já temos um usuario cadastrado com esse nome e sobrenome')
        return render(request, 'paginas/cadastro.html')

    messages.add_message(request, messages.SUCCESS, 'Registrado com sucesso. Agora entre na sua conta')
    user = User.objects.create_user(username=username, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('entrar')


def home(request):
    pass


def entrar(request):
    return render(request, 'paginas/entrar.html')
