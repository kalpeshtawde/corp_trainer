from django.views import generic
from django.shortcuts import render
from .forms import RegistrationForm
from .models import Profile


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'


class SignupView(generic.TemplateView):
    template_name = 'trainer/sign_up.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'

    def get_queryset(self):
        return Profile.objects.all()


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'trainer/detail.html'


def registration(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        p = Profile(
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password')
        )
        p.save()

    context = {
        "form": form,
    }
    return render(request, "trainer/sign_up.html", context)