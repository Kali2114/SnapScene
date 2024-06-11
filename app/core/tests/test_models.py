"""
Test for database models.
"""
from django.test import TestCase
from django.contrib.auth.models import User

from core import models


def create_user(email='example@test.com', password='Test123'):
    """Create and return a new user."""
    return User.objects.create_user(
        email=email,
        password=password,
    )


class ModelTest(TestCase):
    """Test case for database models."""
    pass