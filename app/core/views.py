"""
Views for core app.
"""
from django.views.generic import ListView

from core.models import Post


class IndexView(ListView):
    """View for index site displaying all posts."""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')