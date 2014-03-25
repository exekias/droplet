from django.conf.urls import patterns, include, url

from nazs.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^achilles/', include('achilles.urls')),

    # TODO make this automatic
    url(r'^core/', include('nazs.core.urls')),
    url(r'^network/', include('nazs.network.urls')),
)
