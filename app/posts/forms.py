"""
Forms for post app.
"""
from django import forms

from core.models import Post


class PostForm(forms.ModelForm):
    """Form for creating and updating posts."""

    class Meta:
        model = Post
        fields = ['title', 'caption', 'image']