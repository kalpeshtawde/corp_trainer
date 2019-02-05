from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db import transaction
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import HttpResponseRedirect



from .forms import *
from .models import *
from .serializers import *


class IndexView(generic.TemplateView):
    template_name = 'trainer/index.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'
    model = Profile

    def get_queryset(self):
        queryset = super(ListingView, self).get_queryset()
        queryset = queryset.prefetch_related('user')

        # admin user not needed to show in user listing
        # queryset = queryset.exclude(User__username='admin')

        if 'search' in self.request.GET:
            queryset = queryset.filter(
                Q(user__first_name__contains=self.request.GET['search']) |
                Q(user__last_name__contains=self.request.GET['search'])
            )

        queryset = queryset.annotate(total_cnt=Count('id'))

        return queryset

    # instead of get_queryset or get, here get_context_data is used
    # without this a form cannot be visible
    # here search box was not visible
    def get_context_data(self, **kwargs):
        context = super(ListingView, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', 'give-default-value')
        context['form'] = SearchForm()
        context['count'] = self.get_queryset().count()
        return context


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'trainer/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        detail_user = Profile.objects.filter(pk=self.kwargs['pk'])[0].user
        context['detail_timeline'] = Timeline.objects.filter(user=detail_user)
        context['detail_experience'] = Experience.objects.filter(user=detail_user)
        context['detail_skill'] = Skill.objects.filter(user=detail_user).values_list(
            'title').annotate(total=Count('title')).order_by('-total')
        context['message_form'] = MessageForm
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

            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('trainer:newacct')

        return render(request, self.template_name, {'form':form})


class MainView(generic.TemplateView):
    template_name = 'trainer/edit_profile.html'

    def get(self, request, *args, **kwargs):
        timeline_form = TimelineForm(self.request.GET or None)
        experience_form = ExperienceForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['timeline_form'] = timeline_form
        context['experience_form'] = experience_form
        context['user_data'] = User.objects.filter(
            pk=self.request.user.id
        ).prefetch_related('profile_set', 'timeline_set')
        return self.render_to_response(context)


class TimelineView(generic.View):
    form_class = TimelineForm
    model = Timeline
    template_name = 'trainer/edit_profile.html'

    def add_skills(self, technologies, user):
        if technologies:
            with transaction.atomic():
                for tech in technologies.split(","):
                    s = Skill(user=user, title=tech.strip(), hours=0)
                    s.save()

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.user = request.user
            timeline.save()
            self.add_skills(request.POST['technology'], timeline.user)
            return redirect('trainer:update')


class ExperienceView(generic.View):
    form_class = ExperienceForm
    model = Experience
    template_name = 'trainer/edit_profile.html'

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('trainer:update')
        else:
            return redirect('trainer:update')


class TimelineDelete(generic.DeleteView):
    model = Timeline
    success_url = reverse_lazy('trainer:update')


def newacct(request):
    return render(request, "trainer/acct_created.html")


@login_required()
def update(request):
    return render(request, "trainer/edit_profile.html")


def inbox(request):
    return render(request, "trainer/inbox.html")


def pagenotfound(request):
    return render(request, "trainer/pagenotfound.html")


def message(request):
    template_name = 'trainer/detail.html'
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            return redirect('trainer:detail', 1)
        else:
            messages.error(request, "Error")


######## Rest Framework ###############

## To avoid the CSRF Token missing or incorrect issue
## https://www.cnblogs.com/AmilyWilly/p/6438448.html
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MessageAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
