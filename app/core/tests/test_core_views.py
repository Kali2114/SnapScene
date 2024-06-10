"""
Tests for core views.
"""
from django.test import TestCase
from django.urls import reverse


class TestCoreViews(TestCase):
    """Test case for the core views."""

    def test_get_index_view(self):
        """Test GET request to the index view."""
        url = reverse('index')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'index.html')