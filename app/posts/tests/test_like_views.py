"""
Test for like views.
"""
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from core import models


def create_user(username='Testname', email='test@example.com', password='testpass123'):
    """Create and return a new user"""
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

def get_like_url(post_pk):
    """Get and return toggle like url."""
    return reverse('toggle_like', args=[post_pk])


class LikeViewTests(TestCase):
    """Test case for like views."""

    def setUp(self):
        self.user = create_user()
        self.client.login(username='Testname', password='testpass123')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        self.post = models.Post.objects.create(
            user=self.user,
            image=image,
            caption='Test Caption',
            title='Test title',
        )

    def test_like_post(self):
        """Test liking a post."""
        url = get_like_url(self.post.pk)
        res = self.client.post(url)

        self.assertEqual(res.status_code, 200)
        exists = models.Like.objects.filter(user=self.user, post=self.post).exists()
        self.assertTrue(exists)

    def test_unlike_post(self):
        """Test unliking a post."""
        models.Like.objects.create(
            user=self.user,
            post=self.post,
        )
        url = get_like_url(self.post.pk)
        res = self.client.post(url)

        self.assertEqual(res.status_code, 200)
        exists = models.Like.objects.filter(
            user=self.user,
            post=self.post,
        ).exists()
        self.assertFalse(exists)
