"""
Views for user app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login

from user import forms


class LoginView(FormView):
    """Views for user login."""
    template_name = 'registration/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """Authenticates and logs in the user if credentials are valid."""
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Login successful.')
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid credentials.')
            return self.form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view to add a logout success message."""
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    """View for user registration."""
    template_name = 'registration/register.html'
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """Save the new user and show success message."""
        form.save()
        messages.success(self.request, 'Registration successful. You can now log in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show error message if the form is invalid."""
        messages.error(self.request, 'Registration failed. Please correct the errors.')
        return super().form_invalid(form)


class UserProfile(LoginRequiredMixin, UpdateView):
    """View for user profile update."""
    model = User
    form_class = forms.UserProfileForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        """Return the current logged-in user."""
        return self.request.user

    def form_valid(self, form):
        """Handle valid form submission."""
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle invalid for submission."""
        messages.error(self.request, 'Profile update failed.')
        return super().form_invalid(form)
