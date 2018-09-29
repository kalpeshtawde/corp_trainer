from django import forms


class SearchForm(forms.Form):
    post = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search', 'class':  'form-control searchbox'}))
