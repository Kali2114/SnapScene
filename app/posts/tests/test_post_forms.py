"""
Test for post forms.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from PIL import Image
import io

from posts.forms import PostForm, CommentForm
from core.models import Post


class TestPostForm(TestCase):
    """Test case for post form."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='Test',
            email='Test@wp.pl',
            password='Test123',
        )
        self.client.login(username='Test', password='Test123')

    def test_create_post_form_valid(self):
        """Test create post with a valid form."""

        image = Image.new('RGB', (100, 100))
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        form_data = {
            'title': 'test title',
            'caption': 'test caption'
        }
        form_files = {'image': photo}
        form = PostForm(data=form_data, files=form_files)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], form_data['title'])
        self.assertEqual(form.cleaned_data['caption'], form_data['caption'])
        self.assertEqual(form.cleaned_data['image'].name, form_files['image'].name)

    def test_create_post_form_invalid(self):
        """Test creating a post with an invalid form."""
        form_data = {
            'title': '',
            'caption': 'test caption',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_comment_form_valid(self):
        """Test creating a comment with a valid form."""
        image = Image.new('RGB', (100, 100))
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )
        post = Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=photo
        )
        form_data = {
            'user': self.user.id,
            'post': post.id,
            'content': 'Test content',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_comment_invalid_data(self):
        """Test creating a comment with invalid form data."""
        form_data = {
            'user': self.user.id,
            'post': '1',
            'content': '',
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())