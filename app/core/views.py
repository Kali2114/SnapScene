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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.full_url = self.request.build_absolute_uri(post.get_absolute_url())
        return context