"""
URL mapping for user app.
"""
from django.urls import path

from user import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout')
]