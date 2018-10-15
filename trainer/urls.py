from django.conf.urls import url
from . import views

app_name = 'trainer'

urlpatterns = [
    # /trainer/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /trainer/listing/
    url(r'^listing/$', views.ListingView.as_view(), name='listing'),

    # /trainer/123/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),

    # /trainer/signup/
    url(r'^signup/$', views.registration, name='signup'),

    # /trainer/newacct/
    url(r'^newacct/$', views.newacct, name='newacct')
]
