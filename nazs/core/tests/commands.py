from django.test import TestCase

from nazs.core.commands import run, CommandException


class CommandsTests(TestCase):
    """
    Test on commands classes
    """

    def test_run(self):
        status, output = run("echo -n test")
        self.assertEqual(status, 0)
        self.assertEqual(output, "test")

    def test_run_fail(self):
        self.assertRaises(CommandException, run, "/bin/false")

    def test_run_background(self):
        p = run("exit 27", background=True)
        p.wait()
        self.assertEqual(p.returncode, 27)
