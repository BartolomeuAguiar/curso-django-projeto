from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return HttpResponse('Home 2')


def contato(request):
    return HttpResponse('Contato')


def sobre(request):
    return HttpResponse('SOBRE')
