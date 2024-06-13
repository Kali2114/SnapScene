"""
Test for post views.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


from django.urls import reverse
from core.models import Post
from PIL import Image
import io


CREATE_POST_URL = reverse('post_create')
# UPDATE_POST_URL = lambda pk: reverse('post_update', args=[pk])

# def create_post_detail_url(post_id):
#     """Create and return post detail url."""
#     return reverse('detail-view', args=[post_id])

class PostViewsTests(TestCase):
    """Test case for post views."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
        )
        self.client.login(username='testuser', password='pass123')

    def test_create_post_successful(self):
        """Test creating a post thtough view."""
        image = Image.new('RGB', (100, 100))
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )
        payload = {
            'title': 'test_title',
            'caption': 'test caption',
            'image': photo,
        }
        res = self.client.post(CREATE_POST_URL, payload)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/')
        post = Post.objects.get(title='test_title')
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.caption, payload['caption'])
        self.assertEqual(post.user.username, self.user.username)


    def test_create_post_invalid_data(self):
        """Test creating a post with invalid data."""
        payload = {
            'title': '',
            'caption': 'test_caption'
        }
        res = self.client.post(CREATE_POST_URL, payload)

        self.assertEqual(res.status_code, 200)
        exists = Post.objects.filter(caption='test_caption').exists()
        self.assertFalse(exists)

