import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control flat-control',
                'name': 'username',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control flat-control',
                'name': 'password',
                'placeholder': 'Password'
            }
        )
    )


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control searchbox',
                'name': 'search',
                'placeholder': 'Find Trainer'
            }
        ),
        required=False
    )


class UserForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'First Name'}
        ),
        required=False
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Last Name'}
        ),
        required=False
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Email'}
        ),
        required=False
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Password'}
        ),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Please enter first name")
        return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Please enter last name")
        return last_name

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Please enter email")
        if not re.match(r'.+@.+\..+', username):
            raise forms.ValidationError("Invalid email id")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Email already registered")
        return username

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Please enter password")
        return password
