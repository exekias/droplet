from django.conf.urls import patterns, url

from droplet.web.views import Home


urlpatterns = patterns(
    '',
    url(r'^interfaces/$',
        Home.as_view(block='network:interfaces'),
        name='interfaces'),
)
