"""
Forms for user app.
"""
from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Form class for login"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    """Form class for registration a new user."""
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2

    def clean_email(self):
        """Check that the email is not already in use."""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')

        return email

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'photo']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already in use.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        if self.cleaned_data.get('photo'):
            user.userprofile.photo = self.cleaned_data['photo']
            user.userprofile.save()

        return user
