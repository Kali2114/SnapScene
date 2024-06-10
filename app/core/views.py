"""
Views for core app.
"""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """View for index site."""
    template_name = 'index.html'