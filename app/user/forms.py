"""
Forms for user app.
"""
from django import forms


class LoginForm(forms.Form):
    """Form class for login"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)