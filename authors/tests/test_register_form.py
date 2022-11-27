# from django.test import TestCase
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


# Create your tests here.
class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type you password'),
        ('password2', 'Repeat you password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        )),
        ('email', 'The e-mail must be valid.'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_labels_is_correct(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(label, current)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write you name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password.'),
        ('email', 'E-mail is required.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'ana'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have 4 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must less than 150 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = ('Password must have at least one uppercase letter,'
               'one lowercase letter and one number. The length should be '
               'at least 8 characters.'
               )
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1234'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and Password2 must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_sent_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User e-mail is alredy in use'
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_creted_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'P1pocaD0ce',
            'password2': 'P1pocaD0ce',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_autenticated = self.client.login(
            username='testuser',
            password='P1pocaD0ce',
        )
        self.assertTrue(is_autenticated)
