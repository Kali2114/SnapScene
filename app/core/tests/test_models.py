"""
Test for database models.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from core import models


def create_user(username='Test', email='example@test.com', password='Test123'):
    """Create and return a new user."""
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )


class ModelTest(TestCase):
    """Test case for database models."""

    def test_create_user_profile(self):
        """Test create user profile successful."""
        photo = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        user = create_user()
        profile = models.UserProfile.objects.get(user=user)

        self.assertEqual(profile.user, user)

