from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

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

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertEqual(len(response_context_recipes), 1)
        self.assertIn('recipe test', content)

    def test_recipe_home_template_not_loads_recipes_not_published(self):
        # Altered atribute is_published to false
        self.make_recipe(is_published=False)
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

    def test_category_template_loads_recipes(self):
        needed_name = 'Bolo de Fubá'
        self.make_recipe(title=needed_name)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        # check if needed _name exists
        self.assertIn(needed_name, content)

    def test_recipe_detail_view_functions_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertTrue(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_not_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_detail_page_template_loads_correct_recipe(self):
        # its necessary a title fo a recipe
        needed_name = 'This is test title for a detail - Its loads one reci pe'
        self.make_recipe(title=needed_name)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        # check if needed _name exists
        self.assertIn(needed_name, content)
