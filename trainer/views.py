from django.http import HttpResponse
from django.template import loader
from .models import Profile


def index(request):
    all_profiles = Profile.objects.all()
    template = loader.get_template('trainer/index.html')
    context = {
        'all_profiles': all_profiles,
    }
    return HttpResponse(template.render(context, request))

def profile_detail(request, profile_id):
    return HttpResponse("<H2>Details for Profile id: {0}</H2>".format(
        profile_id))