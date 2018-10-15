from django.views import generic
from django.shortcuts import render
from .forms import RegistrationForm, SearchForm
from .models import Profile


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'


class SignupView(generic.TemplateView):
    template_name = 'trainer/sign_up.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'
    model = Profile

    def get_queryset(self):
        queryset = super(ListingView, self).get_queryset()
        if 'search' in self.request.GET:
            queryset = queryset.filter(first_name=self.request.GET['search'])
        return queryset

    # instead of get_queryset or get, here get_context_data is used
    # without this a form cannot be visible
    # here search box was not visible
    def get_context_data(self, **kwargs):
        context = super(ListingView, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', 'give-default-value')
        context['form'] = SearchForm()
        return context


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


def newacct(request):
    return render(request, "trainer/acct_created.html")
