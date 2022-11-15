from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_functions_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertTrue(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>NADA PARA MOSTRAR AQUI 🐛</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_category_view_functions_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTrue(view.func, views.category)

    def test_recipe_category_view_returns_404_if_not_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_functions_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTrue(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_not_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
