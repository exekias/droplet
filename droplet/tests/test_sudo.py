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
from unittest import skipIf

from droplet.sudo import root, set_euid

import tempfile
import shutil
import os


class SudoTests(TestCase):
    """
    Test droplet.core.sudo module
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        with root():
            shutil.rmtree(self.tmpdir)

    @skipIf(os.geteuid() == 0, "Cannot test set_euid, we are root")
    def test_with_root(self):
        set_euid()
        self.assertNotEqual(os.geteuid(), 0)

        with root():
            self.assertEqual(os.getuid(), 0)

    @skipIf(os.geteuid() == 0, "Cannot test set_euid, we are root")
    def test_no_root(self):
        set_euid()
        self.assertNotEqual(os.geteuid(), 0)

        self.assertRaises(OSError, os.chown, self.tmpdir, 0, 0)
