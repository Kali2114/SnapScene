"""
Views for posts app.
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import edit, DetailView, ListView

from django.views import View
from django.urls import reverse_lazy, reverse

from posts.forms import PostForm, CommentForm
from core.models import Post, Like, Comment


class UserPostView(ListView):
    """View for user posts."""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Queryset displaying only logged user posts."""
        return (Post.objects.filter(user=self.request.user)
                .select_related('user').order_by('-created'))


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
    """View for delete posts."""
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        return context


class PostDetailView(DetailView):
    """View for detail post."""
    model = Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('user').prefetch_related('likes', 'comment_set__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        context['comments'] = (Comment.objects.filter(post=post).select_related('user')
                               .order_by('-created'))
        context['likes_count'] = post.likes.count()
        context['liked'] = post.likes.filter(user=user).exists() if user.is_authenticated else False
        return context


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

    def get(self, request, *args, **kwargs):
        """Handle GET request to get the total number of likes for a post."""
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        return JsonResponse({'total_likes': post.likes.count})

class CommentCreateView(edit.CreateView):
    """View for create comments."""
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_create.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['post_pk']
        return super().form_valid(form)


class CommentUpdateView(edit.UpdateView):
    """View for update comments."""
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_create.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_pk']})

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_pk')
        return Comment.objects.get(pk=comment_id)

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CommentDeleteView(edit.DeleteView):
    """View for delete posts."""
    model = Comment
    template_name = 'comment/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_pk']})

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_pk')
        return Comment.objects.get(pk=comment_id)

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        context['post'] = post
        return context