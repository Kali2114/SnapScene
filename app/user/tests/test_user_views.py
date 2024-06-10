"""
Tests for user views.
"""
from django.test import TestCase
from django.urls import reverse

from user.forms import LoginForm


class PublicUserViewsTests(TestCase):
    """Test case for public user views."""

    def setUp(self):
        self.login_url = reverse('login')

    def test_get_login_view(self):
        """Test GET request to the login view."""
        res = self.client.get(self.login_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'login.html')
        self.assertIsInstance(res.context['form'], LoginForm)

    def test_login_view_post_invalid(self):
        """Test POST request to the login view with invalid data."""
        payload = {
            'username': 'invalid',
            'password': 'invalid',
        }
        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'login.html')
        self.assertFalse(res.context['form'].is_valid())
        self.assertContains(res, 'Invalid credentials.')


"""
Tests for private user views.
"""
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class PrivateUserViewsTests(TestCase):
    """Test case for private user views."""

    def setUp(self):
        self.user = User.objects.create_user(username='Test Name', password='Test123')
        self.client.login(username='Test Name', password='Test123')
        self.index_url = reverse('index')
        self.logout_url = reverse('logout')

    def test_login_view_post_valid(self):
        """Test POST request to the login view with valid data."""
        payload = {
            'username': 'Test Name',
            'password': 'Test123',
        }
        res = self.client.post(reverse('login'), payload)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.index_url)
        self.assertTrue(self.client.login(username='Test Name', password='Test123'))

    def test_logout_view(self):
        """Test that logout view logs out user and redirects to index."""
        res = self.client.post(self.logout_url)
        self.assertRedirects(res, self.index_url)
        self.assertNotIn('_auth_user_id', self.client.session)