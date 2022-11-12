from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views

# Create your tests here.


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correctly(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correctly(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_url_is_correctly(self):
        url = reverse('recipes:recipe', kwargs={'id': 5})
        self.assertEqual(url, '/recipes/5/')


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_functions_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func, views.home)

    def test_recipe_category_view_functions_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTrue(view.func, views.category)

    def test_recipe_detail_view_functions_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTrue(view.func, views.recipe)
