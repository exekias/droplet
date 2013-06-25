from django.test import TestCase

from nazs.core.commands import run
import subprocess

class CommandsTests(TestCase):
    """
    Test on commands classes
    """

    def test_run(self):
        output = run("echo -n test")
        self.assertEqual(output, "test")

    def test_run_fail(self):
        self.assertRaises(subprocess.CalledProcessError, run, "/bin/notexist")

