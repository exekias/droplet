from django.test import TestCase
from django.db.models import loading
from django.core.management import call_command

from nazs.core.models import Model, ModuleInfo
from django.db import models

import sys
import new


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
