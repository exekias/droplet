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

from django.test import TestCase

from nazs import catalog


class CatalogTests(TestCase):
    """
    Test on catalog
    """
    @classmethod
    def setUpClass(cls):
        class Interface1(catalog.NAZSInterface):
            pass

        class Interface2(catalog.NAZSInterface):
            pass

        cls.interface1 = Interface1
        cls.interface2 = Interface2

    def setUp(self):
        self.catalog = catalog.LocalCatalog()

    def test_register_instance_one_superclass(self):
        class A(self.interface1):
            pass

        a = A()
        a.register()
        self.assertEqual(self.catalog.get_instances(self.interface1), set([a]))

        a.unregister()
        self.assertEqual(self.catalog.get_instances(self.interface1), set())

    def test_register_two_instances(self):
        class Interface(self.interface1):
            pass

        a = Interface()
        a.register()

        b = Interface()
        b.register()
        self.assertEqual(self.catalog.get_instances(self.interface1),
                         set([a, b]))

        a.unregister()
        self.assertEqual(self.catalog.get_instances(self.interface1), set([b]))

        b.unregister()
        self.assertEqual(self.catalog.get_instances(self.interface1), set())

    def test_register_instance_multiple_superclasses(self):
        class A(self.interface1, self.interface2):
            pass

        a = A()
        a.register()
        self.assertEqual(self.catalog.get_instances(self.interface1), set([a]))
        self.assertEqual(self.catalog.get_instances(self.interface2), set([a]))

        a.unregister()
        self.assertEqual(self.catalog.get_instances(self.interface1), set())
        self.assertEqual(self.catalog.get_instances(self.interface2), set())

    def test_no_double_register(self):
        class A(self.interface1):
            pass

        a = A()
        a.register()
        a.register()
        a.register()
        self.assertEqual(self.catalog.get_instances(self.interface1), set([a]))

        a.unregister()
        self.assertEqual(self.catalog.get_instances(self.interface1), set())
