"""
Views for posts app.
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import edit, DetailView, ListView

from django.views import View
from django.urls import reverse_lazy

from posts.forms import PostForm
from core.models import Post, Like


class UserPostView(ListView):
    """View for user posts."""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Queryset displaying only logged user posts."""
        return Post.objects.filter(user=self.request.user).order_by('-created')

class PostCreateView(edit.CreateView):
    """View for create posts."""
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDeleteView(edit.DeleteView):
    """View fo delete posts."""
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        """Return queryset listed to user"""
        return Post.objects.filter(user=self.request.user)


class PostUpdateView(edit.UpdateView):
    """View for update posts."""
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        """Return queryset listed to user"""
        return Post.objects.filter(user=self.request.user)


class PostDetailView(DetailView):
    """View for detail post."""
    model = Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'


@method_decorator(login_required, name='dispatch')
class ToggleLikeView(View):
    """View to toggle the like status of a post."""

    def handle_like(self, request, post):
        """Helper method to handle like/unlike logic."""
        if Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.filter(user=request.user, post=post).delete()
            return False
        else:
            Like.objects.create(user=request.user, post=post)
            return True

    def post(self, request, *args, **kwargs):
        """Handle POST request to like or unlike a post."""
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        liked = self.handle_like(request, post)
        return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})

    def delete(self, request, *args, **kwargs):
        """Handle DELETE request to unlike a post."""
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        liked = self.handle_like(request, post)
        return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})