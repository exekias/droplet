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

from django.test import TestCase
from django.template import Template

from droplet import files

import tempfile
import shutil
import os
import pwd
import grp


class FilesTests(TestCase):
    """
    Test on files classes
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_file_write(self):
        filename = os.path.join(self.tmpdir, 'test')
        self.assertFalse(os.path.exists(filename))

        files.ConfFile(filename).write()

        self.assertTrue(os.path.exists(filename))

    def test_file_permissions(self):
        filename = os.path.join(self.tmpdir, 'test')
        self.assertFalse(os.path.exists(filename))

        USER = 'daemon'
        GROUP = 'daemon'
        MODE = 0007
        uid = pwd.getpwnam(USER).pw_uid
        gid = grp.getgrnam(USER).gr_gid

        files.ConfFile(filename,
                       user=USER,
                       group=GROUP,
                       mode=MODE).write()

        stat = os.stat(filename)
        self.assertEqual(stat.st_mode & 0777, MODE)
        self.assertEqual(stat.st_uid, uid)
        self.assertEqual(stat.st_gid, gid)

    def test_overwrite_permissions(self):
        filename = os.path.join(self.tmpdir, 'test')

        USER = 'daemon'
        GROUP = 'daemon'
        uid = pwd.getpwnam(USER).pw_uid
        gid = grp.getgrnam(GROUP).gr_gid

        files.ConfFile(filename).write()

        stat = os.stat(filename)
        self.assertNotEqual(stat.st_uid, uid)
        self.assertNotEqual(stat.st_gid, gid)

    def test_basic_template(self):
        filename = os.path.join(self.tmpdir, 'test')

        # mock get_template
        files.get_template = lambda x: Template(u'hello {{world}}')

        files.TemplateConfFile(filename,
                               template='the template file',
                               template_params={'world': 'foo'}).write()

        self.assertEqual(open(filename).read(), 'hello foo')

    def test_callable_params_template(self):
        filename = os.path.join(self.tmpdir, 'test')

        # mock get_template
        files.get_template = lambda x: Template(u'hello {{world}}')

        def params():
            return {'world': 'bar'}

        files.TemplateConfFile(filename,
                               template='the template file',
                               template_params=params).write()

        self.assertEqual(open(filename).read(), 'hello bar')
