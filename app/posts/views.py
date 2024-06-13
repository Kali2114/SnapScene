"""
Views for posts app.
"""
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
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


class PostDeleteView(DeleteView):
    """View fo delete posts."""
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        """Return queryset listed to user"""
        return Post.objects.filter(user=self.request.user)


class PostUpdateView(UpdateView):
    """View for update posts."""
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        """Return queryset listed to user"""
        return Post.objects.filter(user=self.request.user)
