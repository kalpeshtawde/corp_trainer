from django import forms
from .models import Profile


class RegistrationForm(forms.Form):
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
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Password'}
        ),
        required=False
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Email'}
        ),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'password']

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

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Please enter password")
        return password

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please enter email")
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': "form-control searchbox", 'placeholder': 'Search'}
        ),
        required=False
    )