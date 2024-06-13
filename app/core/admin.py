"""
Custom admin for app.
"""
from django.contrib import admin

from core import models


admin.site.register(models.UserProfile)
admin.site.register(models.Post)