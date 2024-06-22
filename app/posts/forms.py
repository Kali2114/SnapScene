"""
Forms for post app.
"""
from django import forms

from core.models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and updating posts."""

    class Meta:
        model = Post
        fields = ['title', 'caption', 'image']


class CommentForm(forms.ModelForm):
    """Form for creating comments."""

    class Meta:
        model = Comment
        fields = ['content']