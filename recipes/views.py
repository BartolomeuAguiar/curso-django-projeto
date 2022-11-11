from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.recipes.factory import make_recipe

from .models import Recipe

# Create your views here.

# Exibe Todas as receitas em formato de lista


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
    })

# Exibe as Receitas Filtradas pela Categoria Selecionada


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id,
                              is_published=True).order_by('-id'))

    category_name = getattr(
        getattr(recipes[0], 'category', None),
        'name',
        'Not Found'
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{category_name} - Category'
    })

# Exibe  apenas Uma receita na página


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     id=id,
    #     is_published=True,
    # ).order_by('-id').first()
    recipe = get_object_or_404(
        Recipe.objects.filter(id=id, is_published=True))

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_datail_page': True,
    })
