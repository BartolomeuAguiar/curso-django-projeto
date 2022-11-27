from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
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
            '<h1>NO RECIPES FOUND HERE 🐛</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertEqual(len(response_context_recipes), 1)
        self.assertIn('recipe test', content)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        # Altered atribute is_published to false
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>NO RECIPES FOUND HERE 🐛</h1>',
            response.content.decode('utf-8')
        )

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        for i in range(18):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 6)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(60):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1a')
            self.assertEqual(response.context['recipes'].number, 1)
