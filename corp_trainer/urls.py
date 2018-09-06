from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^trainer/', include('trainer.urls')),
    url(r'^trainer/name/', include('trainer.urls')),
]
