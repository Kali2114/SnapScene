"""
Test for comment views.
"""
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from core import models


def create_user(username='Testname', email='test@example,com', password='Test123'):
    """Create and return a new user."""
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

def get_post_url(post_pk):
    """Get and return post url."""
    return reverse('detail', args=[post_pk])


class CommentViewTests(TestCase):
    """Test case for comment views."""

    def setUp(self):
        self.user = create_user()
        self.client.login(username='Testname', password='Test123')
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

    def test_create_comment(self):
        """Test create comment successful."""
        payload = {
            'user': self.user.id,
            'post': self.post.id,
            'content': 'Test content.',
        }
        url = reverse('comment_create', args=[self.post.pk])
        res = self.client.post(url, data=payload)

        self.assertEqual(res.status_code, 302)
        exists = models.Comment.objects.filter(post=self.post).exists()
        self.assertTrue(exists)

    def test_update_comment(self):
        """Test update comment successful."""
        comment = models.Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test content.',
        )
        payload = {'content': 'Update content.'}
        url = reverse('comment_update', args=[comment.post.pk, comment.pk])
        res = self.client.post(url, data=payload)

        self.assertEqual(res.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, payload['content'])

    def test_update_comment_invalid_data(self):
        """Test update comment with invalid data failed."""
        user2 = create_user(username='User123', email='test1@gmail.com', password='Pass123')
        comment = models.Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test content.',
        )
        payload = {
            'user': user2,
            'content': '',
        }
        url = reverse('comment_update', args=[comment.post.pk, comment.pk])
        res = self.client.put(url, data=payload)

        self.assertEqual(res.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Test content.')
        self.assertEqual(comment.user, self.user)

    def test_delete_comment(self):
        """Test delete comment successful."""
        comment = models.Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test content.',
        )
        url = reverse('comment_delete', args=[comment.post.pk, comment.pk])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, 302)
        exists = models.Comment.objects.filter(post=self.post).exists()
        self.assertFalse(exists)
