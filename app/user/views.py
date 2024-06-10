"""
Views for user app.
"""
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView

from django.contrib import messages
from django.contrib.auth import authenticate, login

from user.forms import LoginForm


class LoginView(FormView):
    """Views for user login."""
    template_name = 'login.html'
    form_class = LoginForm
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
