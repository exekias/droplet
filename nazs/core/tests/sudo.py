from django.test import TestCase

from nazs.core.sudo import root

import os

class SudoTests(TestCase):
    """
    Test nazs.core.sudo module
    """

    def test_with_root(self):
        self.assertNotEqual(os.geteuid(), 0)

        with root():
            self.assertEqual(os.getuid(), 0)

