from django.test import TestCase
from django.dispatch import receiver

from nazs.core.module import Module
from nazs.core.files import BaseConfFile
from nazs.core.commands import run
from nazs.core.signals import pre_enable, post_enable, \
                              pre_disable, post_disable

import tempfile
import shutil
import os
import pwd
import grp
import subprocess

class ModuleTests(TestCase):
    """
    Base Module class testing
    """

    def setUp(self):
        class aModule(Module):
            def __init__(self):
                super(aModule, self).__init__()
                self.enable_count = 0
                self.first_enable_count = 0

            def first_enable(self):
                self.first_enable_count += 1

            def enable(self):
                self.enable_count += 1

        self.aModule = aModule

    def test_instance_module(self):
        self.aModule()

    def test_enable_module(self):
        m = self.aModule()
        m.enable()
        self.assertTrue(m.enabled)

    def test_persistent_status(self):
        m = self.aModule()
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

        m.enable()
        self.assertEqual(m.called, 1)

    def test_first_enable_signal(self):
        m = self.aModule()
        m.enable()
        self.assertEqual(m.first_enable_count, 1)
        self.assertEqual(m.enable_count, 1)

        m.disable()
        m.enable()

        self.assertEqual(m.first_enable_count, 1)
        self.assertEqual(m.enable_count, 2)

    def test_double_actions(self):
        m = self.aModule()
        self.assertFalse(m.enabled)

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

        BaseConfFile(filename).write()

        self.assertTrue(os.path.exists(filename))

    def test_file_permissions(self):
        filename = os.path.join(self.tmpdir, 'test')
        self.assertFalse(os.path.exists(filename))

        USER = 'daemon'
        GROUP = 'daemon'
        MODE = 0007
        uid = pwd.getpwnam(USER).pw_uid
        gid = grp.getgrnam(USER).gr_gid

        BaseConfFile(filename,
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
        gid = grp.getgrnam(USER).gr_gid

        BaseConfFile(filename).write()

        stat = os.stat(filename)
        self.assertNotEqual(stat.st_uid, uid)
        self.assertNotEqual(stat.st_gid, gid)


class CommandsTests(TestCase):
    """
    Test on commands classes
    """

    def test_run(self):
        output = run("echo -n test")
        self.assertEqual(output, "test")

    def test_run_fail(self):
        self.assertRaises(subprocess.CalledProcessError, run, "/bin/notexistent")

