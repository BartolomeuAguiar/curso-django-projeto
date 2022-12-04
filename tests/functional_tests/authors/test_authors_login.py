import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_success(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # user vê o formulário
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # insere as credenciais
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # usuario envia o form
        form.submit()
        self.assertIn(f'Your are logged in with { user.username }',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
        # fim do teste

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        # self.sleep(10)
        self.assertIn('Not Found',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        # user abre a pagina de login
        self.browser.get(
            self.live_server_url+reverse('authors:login')
        )
        # user ver o formulario  de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        # user tenta enviar dados vazios
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('  ')
        password.send_keys('   ')
        form.submit()
        # vê mensa
        self.assertIn('Invalid username or password',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid_credentials(self):

        # user abre a pagina de login
        self.browser.get(
            self.live_server_url+reverse('authors:login')
        )
        # user ver o formulario  de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        # user tenta enviar dados errados
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('user')
        password.send_keys('P@ssw.rd')
        form.submit()
        # vê mensa
        self.assertIn('Invalid credentials',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
