from django.test import TestCase
from django.template import Template

from nazs.core import files

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

        files.BaseConfFile(filename).write()

        self.assertTrue(os.path.exists(filename))

    def test_file_permissions(self):
        filename = os.path.join(self.tmpdir, 'test')
        self.assertFalse(os.path.exists(filename))

        USER = 'daemon'
        GROUP = 'daemon'
        MODE = 0007
        uid = pwd.getpwnam(USER).pw_uid
        gid = grp.getgrnam(USER).gr_gid

        files.BaseConfFile(filename,
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

        files.BaseConfFile(filename).write()

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
