from django import forms
from .models import Profile


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'First Name'}
        )
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Last Name'}
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Password'}
        )
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': "form-control flat-control", 'placeholder': 'Email'}
        )
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self, *args, **kwargs):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not first_name:
            print("----------{}".format(first_name))
            raise forms.ValidationError("First name cannot be blanked")
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email
