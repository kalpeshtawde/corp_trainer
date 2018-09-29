from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile

from trainer.forms import SearchForm


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'

    def get_queryset(self):
        return Profile.objects.all()


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'trainer/detail.html'


class SearchView(generic.TemplateView):
    template_name = 'trainer/navbar.html'

    def get_queryset(self):
        return Profile.objects.all()

    def get(self, request):
        form = SearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SearchForm(request.POST, auto_id=False)

        if form.is_valid():
            text = form.cleaned_data['post']

        args = {'form': form, 'search': text}
        return render(request, self.template_name, args)


class ProfileCreate(CreateView):
    model = Profile
    fields = ['first_name', 'last_name', 'country', 'photo', 'rating']
