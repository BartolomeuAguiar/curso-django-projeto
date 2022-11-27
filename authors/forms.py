import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter,'  # noqa:E501
                              'one lowercase letter and one number. The length should be '  # noqa:E501
                               'at least 8 characters.'
                               ),
                              code='invalid'
                              )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type you password')
        add_placeholder(self.fields['password2'], 'Repeat you password')

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have 4 characters',
            'max_length': 'Username must less than 150 characters',
        },
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        min_length=4,
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        label='Password',
        validators=[strong_password],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please repeat your password.'
        },
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write you name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write you last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required.'},
        label='E-mail',
        help_text=('The e-mail must be valid.'),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is alredy in use', code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and Password2 must be equal',
                code='invalid')
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            })
