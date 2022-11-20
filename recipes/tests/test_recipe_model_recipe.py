from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raise_error_if_has_more_65_chars(self):
        self.recipe.title = 'A'*70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
