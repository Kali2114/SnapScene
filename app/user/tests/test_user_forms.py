"""
Test for user forms.
"""
import io
from django.test import TestCase

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from user import forms


def get_temporary_image():
    """Create and return a temporary image file."""
    image = Image.new('RGB', (100, 100))
    tmp_file = io.BytesIO()
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)
    return SimpleUploadedFile('test_image.jpg', tmp_file.read(), content_type='image/jpeg')


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


class TestUserProfileUpdate(TestCase):
    """Test case for the profile update form."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='test name',
            email='test@example.com',
            password='test123',
        )
        # Create a valid image file
        self.photo = get_temporary_image()
        self.valid_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
        }
        self.invalid_data = {
            'username': '',
            'email': '',
        }

    def test_form_valid_data(self):
        """Test that the form is valid with correct data."""
        form = forms.UserProfileForm(data=self.valid_data, files={'photo': self.photo}, instance=self.user)
        user = form.save()
        user.refresh_from_db()

        self.assertTrue(form.is_valid())
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.userprofile.photo)

    def test_form_invalid_data(self):
        """Test that the form is invalid with incorrect data."""
        form = forms.UserProfileForm(data=self.invalid_data, instance=self.user)

        self.assertFalse(form.is_valid())

        user = form.save()
        user.refresh_from_db()

        if not form.is_valid():
            print("Form errors:", form.errors)

        self.assertTrue(form.is_valid())
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertTrue(user.userprofile.photo)

    def test_form_invalid_data(self):
        """Test that the form is invalid with incorrect data."""
        form = forms.UserProfileForm(data=self.invalid_data, instance=self.user)
        self.assertFalse(form.is_valid())
