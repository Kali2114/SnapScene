"""
ULRs mapping post app.
"""
from django.urls import path

from posts import views


urlpatterns = [
    path('create', views.PostCreateView.as_view(), name='post_create')
]