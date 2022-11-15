from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='criado_test',
                    username='usernumber1',
                    password='usernumber1',
                    email='usernumber1@user.com',
                    ):
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='recipe test',
        description='lorem ipsum dolor',
        slug='recipe-test',
        preparation_time=5,
        preparation_time_unit='minutos',
        servings=3,
        servings_unit='fatias',
        preparation_steps='um texto bem grande deve vir aqui',
        preparation_steps_is_html=False,
        is_published=True,
        cover='/'
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover,
        )
