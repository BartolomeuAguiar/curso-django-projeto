from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/home.html')


def contato(request):
    return render(request, 'recipes/contato.html')


def sobre(request):
    return render(request, 'recipes/sobre.html')
