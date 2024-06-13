"""
Views for posts app.
"""
from django.views.generic.edit import (
    CreateView,
)

from django.urls import reverse_lazy

from posts.forms import PostForm
from core.models import Post


class PostCreateView(CreateView):
    """View for create posts."""
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
