from django.conf.urls import url
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm


app_name = 'trainer'

urlpatterns = [
    # /trainer/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /trainer/login/
    url(r'^login/$', LoginView.as_view(template_name='trainer/login.html', authentication_form=LoginForm), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='trainer/user_listing.html'), name='logout'),

    # /trainer/listing/
    url(r'^listing/$', views.ListingView.as_view(), name='listing'),

    # /trainer/123/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),

    # /trainer/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /trainer/newacct/
    url(r'^newacct/$', views.newacct, name='newacct'),

    # /trainer/inbox
    url(r'^inbox/$', views.inbox, name='inbox'),

    # /trainer/message
    url(r'^message/$', views.message, name='message'),

    # /trainer/update
    url(r'^update/$', views.MainView.as_view(), name='update'),
    url(r'^skill/$', views.SkillView.as_view(), name='skill'),
    url(r'^availability/$', views.AvailabilityView.as_view(), name='availability'),
    url(r'^timeline/$', views.TimelineView.as_view(), name='timeline'),
    url(r'^experience/$', views.ExperienceView.as_view(), name='experience'),

    # /trainer/update/123/delete
    url(r'^update/timeline/(?P<pk>[0-9]+)/delete/$', views.TimelineDelete.as_view(), name='timeline-delete'),
    url(r'^update/skill/(?P<pk>[0-9]+)/delete/$', views.SkillDelete.as_view(), name='skill-delete'),

    # /trainer/pagenotfound
    url(r'^pagenotfound/$', views.pagenotfound, name='pagenotfound'),

    # Rest framework urls
    url(r'^api/message', views.MessageAPIView.as_view(), name='api_message'),

]
