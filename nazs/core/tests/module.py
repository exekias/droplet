from django.test import TestCase
from django.dispatch import receiver

from nazs.core.module import Module
from nazs.core.signals import pre_enable, post_enable, \
                              pre_disable, post_disable

class ModuleTests(TestCase):
    """
    Base Module class testing
    """

    def setUp(self):
        class aModule(Module):
            def __init__(self):
                super(aModule, self).__init__()
                self.enable_count = 0
                self.install_count = 0

            def install(self):
                self.install_count += 1

            def enable(self):
                self.enable_count += 1

        self.aModule = aModule

    def test_instance_module(self):
        self.aModule()

    def test_enable_module(self):
        m = self.aModule()
        m.install()
        m.enable()
        self.assertTrue(m.enabled)

    def test_assure_installed(self):
        m = self.aModule()
        self.assertRaises(AssertionError, m.enable)

    def test_persistent_status(self):
        m = self.aModule()
        m.install()
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

        m.install()
        m.enable()
        self.assertEqual(m.called, 1)

    def test_double_actions(self):
        m = self.aModule()
        self.assertFalse(m.enabled)

        m.install()

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

