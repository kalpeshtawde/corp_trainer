from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SearchForm, UserForm, TimelineForm
from .models import Profile, Timeline


class IndexView(generic.ListView):
    template_name = 'trainer/index.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'
    model = Profile

    def get_queryset(self):
        queryset = super(ListingView, self).get_queryset().prefetch_related("user")

        # admin user not needed to show in user listing
        # queryset = queryset.exclude(User__username='admin')

        if 'search' in self.request.GET:
            queryset = queryset.filter(
                Q(user__first_name__contains=self.request.GET['search']) |
                Q(user__last_name__contains=self.request.GET['search'])
            )
        return queryset

    # instead of get_queryset or get, here get_context_data is used
    # without this a form cannot be visible
    # here search box was not visible
    # def get_context_data(self, **kwargs):
    #     context = super(ListingView, self).get_context_data(**kwargs)
    #     context['search'] = self.request.GET.get('search', 'give-default-value')
    #     #context['form'] = SearchForm()
    #     return context


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'trainer/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(DetailView, self).get_context_data(**kwargs)
    #     context['search'] = self.request.GET.get('search', 'give-default-value')
    #     context['form'] = SearchForm()
    #     return context


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

            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('trainer:newacct')

        return render(request, self.template_name, {'form':form})


class TimelineView(generic.ListView):
    form_class = TimelineForm
    model = Timeline
    template_name = 'trainer/edit_profile.html'

    def get_queryset(self):
        queryset = super(TimelineView, self).get_queryset().order_by('-from_date')
        return queryset

    # Without this form input fields are not visible
    # Here the form is returned
    def get_context_data(self, **kwargs):
        context = super(TimelineView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(None)
        return context

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.user = request.user
            timeline.save()
            return redirect('trainer:update')


def newacct(request):
    return render(request, "trainer/acct_created.html")

@login_required()
def update(request):
    return render(request, "trainer/edit_profile.html")