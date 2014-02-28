from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from nazs.web.views import ModulesView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="web/home.html")),
    url(r'^modules/$', ModulesView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
