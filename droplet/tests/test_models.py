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

from droplet.models import ModuleInfo


class ModelTests(TestCase):
    """
    Models class testing
    """
    def test_0_counters(self):
        self.assertEqual(ModuleInfo.objects.count(), 0)
        self.assertEqual(ModuleInfo.objects.all().count(), 0)
        self.assertEqual(ModuleInfo.objects.new().count(), 0)
        self.assertEqual(ModuleInfo.objects.changed().count(), 0)
        self.assertEqual(ModuleInfo.objects.deleted().count(), 0)

    def test_all_counter(self):
        ModuleInfo(name='a').save()
        self.assertEqual(ModuleInfo.objects.count(), 1)

        ModuleInfo(name='b').save()
        self.assertEqual(ModuleInfo.objects.all().count(), 2)

    def test_deleted_counter(self):
        a = ModuleInfo()
        a.save()
        self.assertEqual(ModuleInfo.objects.deleted().count(), 0)

        a.delete()

        # no longer under objects.all()
        self.assertEqual(ModuleInfo.objects.count(), 0)

        # but in deleted
        self.assertEqual(ModuleInfo.objects.deleted().count(), 1)

        ModuleInfo.commit()

        # Totally deleted
        self.assertEqual(ModuleInfo.objects.deleted().count(), 0)

    def test_new_changed_counters(self):
        a = ModuleInfo(name='a')
        a.save()
        b = ModuleInfo(name='b')
        b.save()
        self.assertEqual(ModuleInfo.objects.changed().count(), 2)
        self.assertEqual(ModuleInfo.objects.new().count(), 2)

        ModuleInfo.commit()
        self.assertEqual(ModuleInfo.objects.changed().count(), 0)
        self.assertEqual(ModuleInfo.objects.new().count(), 0)

        a = ModuleInfo.objects.all()[0]
        a.name = 'new name'
        a.save()

        self.assertEqual(ModuleInfo.objects.new().count(), 0)
        self.assertEqual(ModuleInfo.objects.changed().count(), 1)

    def test_update(self):
        ModuleInfo(name='a').save()
        ModuleInfo(name='b').save()
        ModuleInfo.commit()

        ModuleInfo.objects.update(status=2)
        self.assertEqual(ModuleInfo.objects.changed().count(), 2)

    def test_delete(self):
        ModuleInfo(name='a').save()
        ModuleInfo(name='b').save()
        ModuleInfo.objects.all().delete()

        self.assertEqual(ModuleInfo.objects.all().count(), 0)
        self.assertEqual(ModuleInfo.objects.deleted().count(), 2)


class ModuleInfoTests(TestCase):
    """
    ModuleInfo model tests
    """
    def test_unicode(self):
        m = ModuleInfo(name='foo')
        self.assertEqual(str(m), 'Module foo')
