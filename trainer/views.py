from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from math import ceil
from operator import and_, or_
from functools import reduce


from .forms import *
from .models import *
from .serializers import *
from .controller import Controller


class IndexView(generic.TemplateView):
    template_name = 'trainer/index.html'


class ListingView(generic.ListView):
    template_name = 'trainer/user_listing.html'
    model = Profile
    paginate_by = 4

    def get_queryset(self):
        queryset = super(ListingView, self).get_queryset()
        queryset = queryset.prefetch_related('user', 'user__availability')

        # admin user not needed to show in user listing
        # queryset = queryset.exclude(User__username='admin')

        if 'search' in self.request.GET:
            search = re.sub('[^a-zA-Z0-9 ]', ' ', self.request.GET['search'])
            search = list(filter(None, search.split(' ')))
            queryset = queryset.filter(reduce(or_, [
                (Q(user__skill__title__contains=q) |
                Q(user__availability__locations__contains=q)) for q in search
                ])).distinct()

        return queryset

    # instead of get_queryset or get, here get_context_data is used
    # without this a form cannot be visible
    # here search box was not visible
    def get_context_data(self, **kwargs):
        context = super(ListingView, self).get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', 'give-default-value')
        context['form'] = SearchForm()
        context['count'] = self.get_queryset().count()
        context['pages'] = range(1, ceil(context['count'] / self.paginate_by) + 1)
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


class RegisterView(generic.View):
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

            authentication_token = get_random_string(length=50)

            # Send activation email to new registered user
            #Controller.send_activation_mail(authentication_token)

            # Add entry to profile model so that it is visible in listing
            profile = Profile(user=user, activation_string=authentication_token)
            profile.save()

            # Set newly created account by default deactivated
            User.objects.filter(id=user.id).update(
                is_active=False
            )

            return redirect('trainer:verifyemail')

        return render(request, self.template_name, {'form':form})


class MainView(generic.TemplateView):
    template_name = 'trainer/edit_profile.html'

    def get(self, request, *args, **kwargs):
        skill_form = SkillForm(self.request.GET or None)
        availability_form = AvailabilityForm(self.request.GET or None)
        timeline_form = TimelineForm(self.request.GET or None)
        experience_form = ExperienceForm(self.request.GET or None)

        context = self.get_context_data(**kwargs)
        context['skill_form'] = skill_form
        context['availability_form'] = availability_form
        context['timeline_form'] = timeline_form
        context['experience_form'] = experience_form
        context['user_data'] = User.objects.filter(
            pk=self.request.user.id
        ).prefetch_related('profile_set', 'timeline_set')
        return self.render_to_response(context)


class SkillView(generic.View):
    form_class = SkillForm
    model = Skill
    template_name = 'trainer/edit_profile.html'

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('trainer:update')


class AvailabilityView(generic.View):
    form_class = AvailabilityForm
    model = Availability
    template_name = 'trainer/edit_profile.html'

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user

            # One user can have only one availability data.
            # Delete existing data
            Availability.objects.filter(user=availability.user).delete()
            availability.save()
            return redirect('trainer:update')



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
            #self.add_skills(request.POST['technology'], timeline.user)
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


class SkillDelete(generic.DeleteView):
    model = Skill
    success_url = reverse_lazy('trainer:update')


class TimelineDelete(generic.DeleteView):
    model = Timeline
    success_url = reverse_lazy('trainer:update')


def newacct(request):
    return render(request, "trainer/acct_created.html")


def verifyemail(request):
    return render(request, "trainer/verify_email.html")


def activation(request):
    try:
        profile = Profile.objects.filter(
            activation_string=request.GET['activation_token'])[0]
    except IndexError:
        return redirect('trainer:listing')

    user = profile.user

    if user:
        user.is_active = True
        profile.activation_string = None
        user.save()
        profile.save()
        return render(request, "trainer/acct_created.html")

    return redirect('trainer:listing')


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
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        BasicAuthentication
    )

    def get(self, request):
        message = Message.objects.filter(user=self.request.user)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def put(self, request):
        instance = Message.objects.get(user=request.user)
        serializer = MessageSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        instance = Message.objects.get(user=request.user)
        serializer = MessageSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailabilityAPIView(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        BasicAuthentication
    )

    def get(self, request):
        availability = Availability.objects.filter(user=request.user)
        serializer = AvailabilitySerializer(availability, many=True)
        return Response(serializer.data)

    def put(self, request):
        instance = Availability.objects.get(user=request.user)
        serializer = AvailabilitySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsAPIView(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        BasicAuthentication
    )

    def get(self, request):
        reviews = Reviews.objects.filter(user=request.user)
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        #instance = Reviews.objects.get(user=request.user)
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
