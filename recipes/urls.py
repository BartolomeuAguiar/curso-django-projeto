from django.urls import path

from recipes.views import contato, home, sobre

urlpatterns = [
    path('', home),
    path('sobre/', sobre),
    path('contato/', contato),
]
