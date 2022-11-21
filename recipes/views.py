from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe

# Create your views here.

# Show all recipes in list format


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    # recipes = get_list_or_404(Recipe.objects.filter(
    #         is_published = True,).order_by('-id')
    #     )
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
    })

# Returns the Recipes filtereds by category


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

# Returns the datailed recipe page


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

# Returns Searchs page


def search(request):
    ...
