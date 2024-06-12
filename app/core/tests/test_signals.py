"""
Tests for signals.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import UserProfile

User = get_user_model()

class UserProfileSignalTest(TestCase):
    """Test case for user profile signals."""

    def test_create_user_creates_profile(self):
        """Test that creating a user also creates a user profile."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
        )
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_save_user_profile(self):
        """Test that saving a user also saves the user profile."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
        )
        user.username = 'updateduser'
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(user_profile.user.username, 'updateduser')