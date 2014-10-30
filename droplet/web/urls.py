# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pkg_resources

from droplet.util import import_module
from django.conf.urls import patterns, include, url
from .views import Home


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^wizard/(?P<block>.*)/$', Home.as_view(), name='wizard'),
    url(r'^achilles/', include('achilles.urls')),
    url(r'^core/', include('droplet.core.urls', namespace='core')),
)

# Add droplet.web modules urls
for app in pkg_resources.iter_entry_points('droplet.app'):
    regex = r'^%s/' % app.name
    path = '%s.urls' % app.module_name
    if import_module(path):
        urlpatterns += patterns('', url(regex, include(path,
                                                       namespace=app.name)))
