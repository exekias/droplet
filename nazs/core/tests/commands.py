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
        self.assertRaises(subprocess.CalledProcessError, run, "/bin/exit 1")

    def test_run_background(self):
        p = run("exit 27", background=True)
        p.wait()
        self.assertEqual(p.returncode, 27)
