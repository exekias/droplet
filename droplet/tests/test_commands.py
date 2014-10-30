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

from droplet.commands import run, CommandException


class CommandsTests(TestCase):
    """
    Test on commands classes
    """

    def test_run(self):
        output = run("echo -n test")
        self.assertEqual(output, "test")

    def test_run_fail(self):
        self.assertRaises(CommandException, run, "/bin/false")

    def test_run_background(self):
        p = run("exit 27", background=True)
        p.wait()
        self.assertEqual(p.returncode, 27)
