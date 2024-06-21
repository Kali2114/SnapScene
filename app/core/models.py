"""
Database models.
"""
from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User

from django.urls import reverse


class UserProfile(models.Model):
    """Model for user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    photo = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """Model for post."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='images/%y/%m/%d')
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get and return absolute URL for post."""
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title

    # def total_likes(self):
    #     """Get and return a count of all likes for post."""
    #     return self.likes.count


class Like(models.Model):
    """Model for likes system."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')