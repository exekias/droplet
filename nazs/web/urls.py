from django.conf.urls import patterns, include, url

from .views import Home


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^wizard/(?P<block>.*)/$', Home.as_view(), name='wizard'),

    url(r'^achilles/', include('achilles.urls')),

    # TODO make this automatic
    url(r'^core/', include('nazs.core.web.urls')),
    url(r'^network/', include('nazs.network.web.urls')),
)
