"""
Views for core app.
"""
from django.views.generic import TemplateView

from core.models import Post


class IndexView(TemplateView):
    """View for index site."""
    template_name = 'index.html'
    queryset = Post.objects.all()