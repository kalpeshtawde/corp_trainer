from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from .forms import LoginForm


app_name = 'trainer'

urlpatterns = [
    # /trainer/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /trainer/login/
    url(r'^login/$', login, {'template_name': 'trainer/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'trainer/registration_form.html'}, name='logout'),

    # /trainer/listing/
    url(r'^listing/$', views.ListingView.as_view(), name='listing'),

    # /trainer/123/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),

    # /trainer/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /trainer/newacct/
    url(r'^newacct/$', views.newacct, name='newacct')
]
