from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'

    def get_queryset(self):
        return Profile.objects.all()


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'trainer/detail.html'


class DetailView(generic.TemplateView):
    template_name = 'trainer/index.html'

    def get(self, request):

class ProfileCreate(CreateView):
    model = Profile
    fields = ['first_name', 'last_name', 'country', 'photo', 'rating']