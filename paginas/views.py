from django.shortcuts import render
from django.contrib import messages


def cadastro(request):
    messages.add_message(request, messages.INFO, 'chave')
    return render(request, 'paginas/cadastro.html')


def home(request):
    pass