import re
from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import *


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
        widget=forms.PasswordInput(
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


class SkillForm(forms.ModelForm):

    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'Enter your skills, one at a time', 'type': 'text'}
        ),
        required=True
    )

    class Meta:
        model = Skill
        fields = ['title']


class AvailabilityForm(forms.ModelForm):

    locations = forms.CharField(
        max_length=2000,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'type': 'text',
                'ng-disabled': 'disableAvailability'
            }
        ),
        required=True,
    )

    hours_per_week = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'type': 'text',
                'ng-disabled': 'disableAvailability'
            }
        ),
        required=True
    )

    class Meta:
        model = Availability
        fields = ['locations', 'hours_per_week']


class TimelineForm(forms.ModelForm):

    organization = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'i.e ABC Limited',
                'type': 'text'
            }
        ),
        required=True
    )
    technology = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'i.e Java, Python', 'type': 'text'}
        ),
        required=True
    )
    from_date = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': "form-control", 'aria-describedby': 'date-addon', 'type': 'text'}
        ),
        required=True
    )

    class Meta:
        model = Timeline
        fields = ['organization', 'technology', 'from_date', 'hours', 'trainee_cnt']

        HOURS_CHOICE = (
            ('< 5', '< 5'),
            ('5 - 10', '5 - 10'),
            ('1 - 20', '10 - 20'),
            ('2 - 30', '20 - 30'),
            ('> 30', '> 30'),
        )
        TRAINEE_CNT= (
            ('1-10', '1-10'),
            ('10-30', '10-30'),
            ('30-50', '30-50'),
            ('50-100', '50-100'),
            ('>100', '>100'),
        )
        widgets = {
            'hours': forms.Select(
                choices=HOURS_CHOICE, attrs={'class': 'form-control'}
            ),
            'trainee_cnt': forms.Select(
                choices=TRAINEE_CNT, attrs={'class': 'form-control'}
            ),
        }


class ExperienceForm(forms.ModelForm):
    organization = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': "form-control", 'rows': 4}
        ),
        required=True
    )
    desc = forms.CharField(
        max_length=2000,
        widget=forms.TextInput(
            attrs={'class': "form-control", 'placeholder': 'i.e ABC Limited', 'type': 'text'}
        ),
        required=True
    )
    #from_date = forms.CharField(max_length=20, required=True)
    #to_date = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Experience
        fields = [
            'organization','desc',
            'from_year', 'from_month',
            'to_year', 'to_month'
        ]

        MONTHNAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        MONTH_CHOICE = tuple((m, m) for m in MONTHNAMES)

        start_year = 1950
        end_year = datetime.now().year + 1
        YEARS_CHOICE = tuple((a, a) for a in range(start_year, end_year)[::-1])

        widgets = {
            'from_year': forms.Select(
                choices=YEARS_CHOICE,
                attrs={
                    'class': "form-control",
                    'aria-describedby': 'date-addon',
                    'type': 'text'
                },
            ),
            'from_month': forms.Select(
                choices=MONTH_CHOICE,
                attrs={
                    'class': "form-control",
                    'aria-describedby': 'date-addon',
                    'type': 'text'
                },
            ),
            'to_year': forms.Select(
                choices=YEARS_CHOICE,
                attrs={
                    'class': "form-control",
                    'aria-describedby': 'date-addon',
                    'type': 'text'
                },
            ),
            'to_month': forms.Select(
                choices=MONTH_CHOICE,
                attrs={
                    'class': "form-control",
                    'aria-describedby': 'date-addon',
                    'type': 'text'
                },
            ),
        }


class MessageForm(forms.Form):

    message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'rows': 5,
                'placeholder': "Provide requirement details like type of training, skills, location, number of days, number of attendants",
                'ng-model': 'message_text'
            }
        ),
        required=False
    )

    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'ng-model': 'message_phone'
            }
        ),
        required=False
    )

    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'ng-model': 'message_email'
            }
        ),
        required=False
    )

    def clean_message(self, *args, **kwargs):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Please enter Message")
        return message
    
    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError("Please enter phone")
        return phone

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not re.match(r'.+@.+\..+', email):
            raise forms.ValidationError("Invalid email id")
        return email
