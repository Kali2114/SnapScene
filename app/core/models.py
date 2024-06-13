"""
Database models.
"""
from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User


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

    def __str__(self):
        return self.title
