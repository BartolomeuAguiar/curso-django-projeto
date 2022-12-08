from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_functions_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTrue(view.func.view_class, views.RecipeListViewCategory)

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

    def test_recipe_category_template_not_loads_recipes_not_published(self):
        # Altered atribute is_published to false
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)
