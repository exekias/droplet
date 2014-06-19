from django.conf.urls import patterns, url

from nazs.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^modules/$', Home.as_view(block='core:modules'), name='modules'),
)
