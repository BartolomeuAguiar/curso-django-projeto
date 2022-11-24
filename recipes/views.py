from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination_range

from .models import Recipe

# Create your views here.

# Show all recipes in list format


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,

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

# Returns in the Search page the recipes that contains the search term


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ), is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}',
        'search_term': search_term,
        'recipes': recipes,
    })
