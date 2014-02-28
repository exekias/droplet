from django.test import TestCase

from nazs.core.sudo import root, set_euid

import tempfile
import shutil
import os


class SudoTests(TestCase):
    """
    Test nazs.core.sudo module
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        with root():
            shutil.rmtree(self.tmpdir)

    def test_with_root(self):
        set_euid()
        self.assertNotEqual(os.geteuid(), 0)

        with root():
            self.assertEqual(os.getuid(), 0)

    def test_no_root(self):
        set_euid()
        self.assertNotEqual(os.geteuid(), 0)

        self.assertRaises(OSError, os.chown, self.tmpdir, 0, 0)
