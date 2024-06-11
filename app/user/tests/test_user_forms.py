"""
Test for user forms.
"""
from django.test import TestCase

from django.contrib.auth.models import User

from user import forms


class TestLoginForm(TestCase):
    """Test case for login form."""

    def test_login_form_valid_data(self):
        """Test that login form is valid with correct data."""
        form = forms.LoginForm(data={
            'username': 'Test Name',
            'password': 'Test123',
        })

        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        """Test that login form is invalid with no data."""
        form = forms.LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_form_invalid_data(self):
        """Test that login form is invalid with empty fields."""
        form = forms.LoginForm(data={
            'name': '',
            'password': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class UserRegistrationFormTests(TestCase):
    """Test case for user registration form."""

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }
        User.objects.create_user(
            username='existing',
            email='existing@com.pl',
            password='Pass1234',
        )

    def test_form_valid_data(self):
        """Test that for is valid with correct data."""
        form = forms.UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_password_do_not_match(self):
        """Test that form raises error when passwords do not match."""
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword'
        form = forms.UserRegistrationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', form.errors.get('password2'))

    def test_form_email_already_exists(self):
        """Test that form raises error when email already exists."""
        data = self.valid_data.copy()
        data['email'] = 'existing@com.pl'
        form = forms.UserRegistrationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('This email is already in use.', form.errors.get('email'))
