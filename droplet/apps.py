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

from django.apps import AppConfig
from django.conf import settings

import pkg_resources
import pwd
import os

from .sudo import set_euid


class dropletConfig(AppConfig):
    name = 'droplet'

    def ready(self):
        # Set env variables
        os.environ['LC_ALL'] = 'C'

        # Enorce proper database and log permissions
        pw = pwd.getpwnam(settings.DROPLET_USER)
        for db in settings.DATABASES.itervalues():
            if 'sqlite' in db['ENGINE']:
                filename = db['NAME']

                # Nothing to do for in memory databases
                if filename == ':memory:':
                    continue

                # touch
                with open(filename, 'a'):
                    os.utime(filename, None)

                os.chown(filename, pw.pw_uid, pw.pw_gid)
                os.chmod(filename, 0600)

        for handler in settings.LOGGING['handlers'].values():
            if 'filename' in handler:
                filename = handler['filename']
                os.chown(filename, pw.pw_uid, pw.pw_gid)

        # Lower permissions
        set_euid()

        # Load all modules
        for app in pkg_resources.iter_entry_points('droplet.app'):
            __import__(app.module_name + '.module')
