from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertTrue(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_not_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_detail_page_template_loads_correct_recipe(self):
        # its necessary a title fo a recipe
        needed_name = 'This is test title for a detail - Its loads one reci pe'
        self.make_recipe(title=needed_name)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')
        # check if needed _name exists
        self.assertIn(needed_name, content)

    def test_recipe_detail_template_not_loads_recipe_not_published(self):
        # Altered atribute is_published to false
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 404)
