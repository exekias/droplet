from django.conf.urls import patterns, url

from nazs.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^modules/$', Home.as_view(block='apache:modules'), name='modules'),
    url(r'^confs/$', Home.as_view(block='apache:confs'), name='confs'),
)
