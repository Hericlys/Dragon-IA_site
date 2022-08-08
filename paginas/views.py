from django.shortcuts import render


def cadastro(request):
    return render(request, 'paginas/cadastro.html')


def home(request):
    pass