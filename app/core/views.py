"""
Views for core app.
"""
from django.db.models import Count, Case, When, IntegerField
from django.views.generic import ListView

from core.models import Post


class IndexView(ListView):
    """View for index site displaying all posts."""
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all().select_related('user').prefetch_related(
            'comment_set__user'
        ).annotate(likes_count=Count('likes')).order_by('-created')
        if user.is_authenticated:
            queryset = queryset.annotate(
                liked=Count(Case(When(likes__user=user, then=1),
                                 defaul=0, output_field=IntegerField()))
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.full_url = self.request.build_absolute_uri(post.get_absolute_url())
        return context