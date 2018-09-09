from django.shortcuts import render, get_object_or_404
from .models import Profile, Skill


def index(request):
    all_profiles = Profile.objects.all()
    context = {'all_profiles': all_profiles}
    return render(request, 'trainer/index.html', context)

def detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    return render(request, 'trainer/detail.html', {'profile': profile})

def favourite(request):
    all_profiles = Profile.objects.all()
    profile = get_object_or_404(all_profiles, pk=request.POST['profile'])
    profile.is_favourite = True
    profile.save()
    context = {'all_profiles': all_profiles}
    return render(request, 'trainer/index.html', context)