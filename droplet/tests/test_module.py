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
from django.dispatch import receiver

from droplet.module import Module
from droplet.signals import pre_enable


class ModuleTests(TestCase):
    """
    Base Module class testing
    """

    def setUp(self):
        class aModule(Module):
            def __init__(self):
                super(aModule, self).__init__()
                self.enable_count = 0
                self.install_called = True

            def install(self):
                self.install_called = True

            def enable(self):
                self.enable_count += 1

        self.aModule = aModule

    def test_instance_module(self):
        self.aModule()

    def test_enable_module(self):
        m = self.aModule()
        m.install()
        self.assertTrue(m.install_called)
        self.assertTrue(m.installed)
        m.enable()
        self.assertTrue(m.enabled)

    def test_double_install(self):
        m = self.aModule()
        m.install()
        self.assertRaises(AssertionError, m.install)

    def test_assure_installed(self):
        m = self.aModule()
        self.assertRaises(AssertionError, m.enable)

    def test_persistent_status(self):
        m = self.aModule()
        m.install()
        m.enable()
        self.assertTrue(m.enabled)

        m.disable()

        m = self.aModule()
        self.assertFalse(m.enabled)

    def test_pre_enable_signal(self):
        m = self.aModule()

        m.called = 0

        @receiver(pre_enable)
        def increment(sender, **kwargs):
            self.assertFalse(sender.enabled)
            sender.called += 1

        m.install()
        m.enable()
        self.assertEqual(m.called, 1)

    def test_double_actions(self):
        m = self.aModule()
        self.assertFalse(m.enabled)

        m.install()

        m.enable()
        self.assertEqual(m.enable_count, 1)

        self.assertRaises(AssertionError, m.enable)
        self.assertEqual(m.enable_count, 1)

        m.disable()
        self.assertRaises(AssertionError, m.disable)

        m.enable()
        self.assertEqual(m.enable_count, 2)

    def test_singleton(self):
        x = self.aModule()
        y = self.aModule()
        self.assertEqual(x, y)
