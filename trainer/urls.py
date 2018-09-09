from django.conf.urls import url
from . import views

app_name = 'trainer'

urlpatterns = [
    # /trainer/
    url(r'^$', views.index, name='index'),

    # /trainer/favourite/
    url(r'^favourite/$', views.favourite, name='favourite'),

    # /trainer/123/
    url(r'^(?P<profile_id>\d+)/$', views.detail, name='detail')
]
