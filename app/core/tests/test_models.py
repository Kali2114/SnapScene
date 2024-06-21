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

    def test_create_post(self):
        """Test create post successful."""
        image = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        user = create_user()
        post = models.Post.objects.create(
            user=user,
            image=image,
            caption='Test Caption',
            title='Test title',
        )

        self.assertEqual(str(post), post.title)
        self.assertEqual(post.slug, 'test-title')
        self.assertTrue(post.created)

    def test_get_absolute_post_url(self):
        """Test get the get_absolute_url method."""
        image = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        user = create_user()
        post = models.Post.objects.create(
            user=user,
            image=image,
            caption='Test Caption',
            title='Test title',
        )
        expected_url = reverse('post_detail', args=[str(post.pk)])
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_create_like(self):
        """Test get a like successful."""
        image = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        user = create_user()
        post = models.Post.objects.create(
            user=user,
            image=image,
            caption='Test Caption',
            title='Test title',
        )
        models.Like.objects.create(
            user=user,
            post=post,
        )

        exists = models.Like.objects.filter(post=post).exists()
        self.assertTrue(exists)