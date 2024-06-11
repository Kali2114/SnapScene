"""
Tests for user views.
"""
from django.test import TestCase
from django.urls import reverse
from django.core import mail

from django.contrib.auth.models import User

from user import forms


class PublicUserViewsTests(TestCase):
    """Test case for public user views."""

    def setUp(self):
        self.login_url = reverse('login')

    def test_get_login_view(self):
        """Test GET request to the login view."""
        res = self.client.get(self.login_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/login.html')
        self.assertIsInstance(res.context['form'], forms.LoginForm)

    def test_login_view_post_invalid(self):
        """Test POST request to the login view with invalid data."""
        payload = {
            'username': 'invalid',
            'password': 'invalid',
        }
        res = self.client.post(self.login_url, payload)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/login.html')
        self.assertFalse(res.context['form'].is_valid())
        self.assertContains(res, 'Invalid credentials.')


class PrivateUserViewsTests(TestCase):
    """Test case for private user views."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='Test Name',
            email='Test@example.com',
            password='Test123',
        )
        self.client.login(username='Test Name', password='Test123')
        self.index_url = reverse('index')
        self.logout_url = reverse('logout')
        self.password_change_url = reverse('password_change')
        self.password_change_done_url = reverse('password_change_done')
        self.password_reset_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.registration_url = reverse('register')

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

    def test_get_password_change_view(self):
        """Test GET request to the password change view."""
        res = self.client.get(self.password_change_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/password_change.html')

    def test_change_password_success(self):
        """Test that change password is success with valid credentials."""
        payload = {
            'old_password': 'Test123',
            'new_password1': 'NewTest123',
            'new_password2': 'NewTest123',
        }
        res = self.client.post(self.password_change_url, payload)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.password_change_done_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewTest123'))

    def test_change_password_invalid(self):
        """Test that change password fails with invalid credentials."""
        payload = {
            'old_password': 'wrongpassword',
            'new_password1': 'NewTest123',
            'new_password2': 'NewTest123',
        }
        res = self.client.post(self.password_change_url, payload)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/password_change.html')
        self.assertFalse(res.context['form'].is_valid())

    def test_change_password_valid(self):
        """Test that change password success with valid credentials."""
        payload = {
            'old_password': 'Test123',
            'new_password1': 'NewTest123',
            'new_password2': 'NewTest123',
        }
        res = self.client.post(self.password_change_url, payload)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.password_change_done_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['new_password1']))

    def test_post_password_reset_invalid_email(self):
        """Test POST request to the password reset with an invalid email."""
        payload = {
            'email': 'wrong@example.com'
        }
        res = self.client.post(self.password_reset_url, payload)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    def test_post_password_reset_valid_email(self):
        """Test POST request to the password reset with valid email."""
        payload = {
            'email': 'Test@example.com'
        }
        res = self.client.post(self.password_reset_url, payload)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 1)

    def test_register_view(self):
        """Test GET request to the registration view."""
        res = self.client.get(self.registration_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/register.html')
        self.assertIsInstance(res.context['form'], forms.UserRegistrationForm)

    def test_register_view_valid_data(self):
        """Test POST request to the registration view with valid data."""
        payload = {
            'username': 'Test_Name1',
            'email': 'example@test.com',
            'password1': 'TestPass123',
            'password2': 'TestPass123',
        }
        res = self.client.post(self.registration_url, payload)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('index'))
        exists_user = User.objects.filter(email=payload['email']).exists()
        self.assertTrue(exists_user)

    def test_register_view_invalid_data(self):
        """Test POST request to the registration view with invalid data."""
        payload = {
            'username': 'Test Name1',
            'email': 'example@test.com',
            'password1': 'TestPass123',
            'password2': 'WrongPass123',
        }
        res = self.client.post(self.registration_url, payload)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'registration/register.html')
        exists_user = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(exists_user)
