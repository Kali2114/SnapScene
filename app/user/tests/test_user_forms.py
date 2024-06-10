"""
Test for user forms.
"""
from django.test import TestCase

from user.forms import LoginForm


class TestLoginForm(TestCase):
    """Test case for login form."""

    def test_login_form_valid_data(self):
        """Test that login form is valid with correct data."""
        form = LoginForm(data={
            'username': 'Test Name',
            'password': 'Test123',
        })

        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        """Test that login form is invalid with no data."""
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_form_invalid_data(self):
        """Test that login form is invalid with empty fields."""
        form = LoginForm(data={
            'name': '',
            'password': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)