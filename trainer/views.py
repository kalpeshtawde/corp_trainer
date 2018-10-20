from django.views import generic
from django.shortcuts import render, redirect
from .forms import SearchForm, UserForm
from .models import Profile


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'
    model = Profile

    def get_queryset(self):
        queryset = super(ListingView, self).get_queryset()
        if 'search' in self.request.GET:
            queryset = queryset.filter(first_name__contains=self.request.GET['search'])
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

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', 'give-default-value')
        context['form'] = SearchForm()
        return context


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'trainer/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('trainer:newacct')

        return render(request, self.template_name, {'form':form})

def newacct(request):
    return render(request, "trainer/acct_created.html")

