from django.urls import path

from recipes.views import home, sobre

urlpatterns = [
    path('', home),
    path('sobre/', sobre)
]
