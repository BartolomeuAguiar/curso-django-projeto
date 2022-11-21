from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category name Testing'
        )
        return super().setUp()

    def test_recipe_category_str_representation(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_category_name_max_length(self):
        self.category.name = 'A' * 67
        with self.assertRaises(ValidationError):
            self.category.full_clean()
