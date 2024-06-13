"""
ULRs mapping post app.
"""
from django.urls import path

from posts import views


urlpatterns = [
    path('create', views.PostCreateView.as_view(), name='post_create'),
    path('delete<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('update<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
]