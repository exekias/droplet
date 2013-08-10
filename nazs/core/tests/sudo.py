from django.test import TestCase
from django.conf import settings

from nazs.core.sudo import root

import os
import pwd

class SudoTests(TestCase):
    """
    Test nazs.core.sudo module
    """

    def test_with_root(self):
        uid = int(pwd.getpwnam(settings.RUN_AS_USER).pw_uid)
        self.assertNotEqual(os.geteuid(), 0)

        with root():
            self.assertEqual(os.getuid(), 0)

