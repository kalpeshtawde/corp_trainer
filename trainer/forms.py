from django import forms


class SearchForm(forms.Form):
    post = forms.CharField()