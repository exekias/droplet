# -*- coding: utf-8 -*-
#
#  NAZS
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


class NAZSConfig(AppConfig):
    name = 'nazs'

    def ready(self):
        # Force proper database permissions (sqlite backend only)
        pw = pwd.getpwnam(settings.NAZS_USER)
        for db in settings.DATABASES.itervalues():
            if db['ENGINE'] == 'django.db.backends.sqlite3':
                db_file = db['NAME']

                # touch
                with open(db_file, 'a'):
                    os.utime(db_file, None)

                os.chown(db_file, pw.pw_uid, pw.pw_gid)
                os.chmod(db_file, 0600)

        # Lower permissions
        set_euid()

        # Load all modules
        for app in pkg_resources.iter_entry_points('nazs.app'):
            __import__(app.module_name + '.module')
