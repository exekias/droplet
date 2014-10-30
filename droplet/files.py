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

from django.template.loader import get_template
from django.template import Context

from .sudo import root
from . import settings

import os
import pwd
import grp
import difflib
import logging

logger = logging.getLogger(__name__)


class ConfFile(object):
    """
    ConfFile is the representation of any configuration file that a module will
    write in order to work
    """
    def __init__(self, path, mode=None, user=None, group=None):
        """
        Instance a ConfFile object

        :param path: Full path of the file
        :param mode: POSIX permissions mode (default: not change)
        :param user: Owner of the file (default: not change)
        :param group: Group of the file (default: not change)
        """
        self.path = path
        self.mode = mode
        self.user = user
        self.group = group

    def write(self):
        """
        Write the file, forcing the proper permissions
        """
        with root():
            self._write_log()
            with open(self.path, 'w') as f:
                # file owner
                os.chown(self.path, self.uid(), self.gid())

                # mode
                if self.mode:
                    oldmask = os.umask(0)
                    os.chmod(self.path, self.mode)
                    os.umask(oldmask)

                f.write(self.contents())

    def contents(self):
        """
        Return contents to write in the file
        """
        return ''

    def _write_log(self):
        """
        Write log info
        """
        logger.info("Writing config file %s" % self.path)

        if settings.DEBUG:
            try:
                old_content = open(self.path, 'r').readlines()
            except IOError:
                old_content = ''

            new_content = self.contents().splitlines(True)
            diff = difflib.unified_diff(old_content, new_content,
                                        fromfile=self.path, tofile=self.path)
            if diff:
                logger.debug('Diff:\n' + ''.join(diff))
            else:
                logger.debug('File not changed')

    def uid(self):
        if self.user is None:
            return -1
        return int(pwd.getpwnam(self.user).pw_uid)

    def gid(self):
        if self.group is None:
            return -1
        return int(grp.getgrnam(self.group).gr_gid)


class TemplateConfFile(ConfFile):
    def __init__(self, path, template=None,
                 template_params={}, *args, **kwargs):
        """
        Template based configuration file

        It behaves like :class:`ConfFile` the conf file taking contents for
        the file from the given template file.

        :params template: Template path
        :params template_params: Dict containing template params or function
            returning them (will be called when writting the file)
        """
        self.template = template
        self.template_params = template_params
        super(TemplateConfFile, self).__init__(path, *args, **kwargs)

    def contents(self):
        template = get_template(self.template)
        if callable(self.template_params):
            params = self.template_params()
        else:
            params = self.template_params
        context = Context(params)
        return template.render(context)
