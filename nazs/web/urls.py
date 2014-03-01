from django.conf.urls import patterns, include, url

from nazs.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^core/', include('nazs.web.core.urls')),
)
