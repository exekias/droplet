from django.utils import unittest
from django.dispatch import receiver


from nazs.core.module import Module
from nazs.core.signals import pre_enable, post_enable, \
                              pre_disable, post_disable

class ModuleTests(unittest.TestCase):
    """
    Base Module class testing
    """

    def setUp(self):
        class aModule(Module):
            def __init__(self):
                super(aModule, self).__init__()
                self.x = 3

        self.aModule = aModule

    def test_instance_module(self):
        self.aModule()

    def test_enable_module(self):
        m = self.aModule()
        m.enable()
        self.assertTrue(m.enabled)

    def test_persistent_status(self):
        m = self.aModule()
        self.assertTrue(m.enabled)

        m.disable()

        m = self.aModule()
        self.assertFalse(m.enabled)

    def test_pre_enable_signal(self):
        m = self.aModule()
        self.assertEqual(m.x, 3)

        @receiver(pre_enable)
        def increment(sender, **kwargs):
            sender.x += 1

        m.enable()
        self.assertEqual(m.x, 4)



