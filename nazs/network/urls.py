from django.conf.urls import patterns, url

from nazs.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^interfaces/$',
        Home.as_view(block='network:interfaces'),
        name='interfaces'),
)
