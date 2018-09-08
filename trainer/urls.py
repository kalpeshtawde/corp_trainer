from django.conf.urls import url
from . import views

urlpatterns = [
    # /trainer/
    url(r'^$', views.index, name='index'),

    # /trainer/123/
    url(r'^(?P<profile_id>\d+)/$', views.profile_detail, name='profile_detail')
]
