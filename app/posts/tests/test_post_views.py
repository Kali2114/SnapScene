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
USER_POST_LIST_URL = reverse('user_post_list')
UPDATE_POST_URL = lambda pk: reverse('post_update', args=[pk])
DELETE_POST_URL = lambda pk: reverse('post_delete', args=[pk])
DETAIL_POST_URL = lambda pk: reverse('post_detail', args=[pk])


class PostViewsTests(TestCase):
    """Test case for post views."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
        )
        image = Image.new('RGB', (100, 100))
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)

        self.photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )
        self.client.login(username='testuser', password='pass123')

    def test_create_post_successful(self):
        """Test creating a post through view."""
        payload = {
            'title': 'test_title',
            'caption': 'test caption',
            'image': self.photo,
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

    def test_delete_post(self):
        """Test deleting a post successful."""
        post = Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        url = DELETE_POST_URL(post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/')
        exists = Post.objects.filter(id=post.id).exists()
        self.assertFalse(exists)

    def test_update_post(self):
        """Test updating post successful."""
        post = Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        payload = {
            'title': 'updated title',
            'caption': 'updated caption',
        }
        url = UPDATE_POST_URL(post.id)
        res = self.client.post(url, payload)
        post.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/')
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.caption, payload['caption'])

    def test_update_user_failed(self):
        """Test that update user is failed."""
        user2 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='pass123',
        )
        post = Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        payload = {'user': user2}
        url = UPDATE_POST_URL(post.id)
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(post.user, self.user)

    def test_detail_post_view(self):
        """Test detail view of a post."""
        post = Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        url = DETAIL_POST_URL(post.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'post/post_details.html')

    def test_user_post_list_view(self):
        """Test that user post list show post limited to user."""
        user2 = User.objects.create_user(
            username='testuser1',
            email='test@example.com',
            password='pass123',
        )
        Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        Post.objects.create(
            user=self.user,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        Post.objects.create(
            user=user2,
            title='testtitle',
            caption='testcatption',
            image=self.photo
        )
        url = USER_POST_LIST_URL
        res = self.client.get(url)

        self.assertEqual(len(res.context['posts']), 2)
