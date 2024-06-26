"""
URLs mapping post app.
"""
from django.urls import path

from posts import views


urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('toggle-like/<int:pk>/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('user_post_list/', views.UserPostView.as_view(), name='user_post_list'),
    path('<int:post_pk>/create_comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:post_pk>/update_comment/<int:comment_pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('<int:post_pk>/delete_comment/<int:comment_pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]