from django.dispatch import receiver

from services import Service
from models import ModuleInfo
from signals import pre_enable, post_enable, \
                    pre_disable, post_disable


class ModuleMeta(type):
    """
    Module metaclass, to allow some black magic tricks on module definitions
    """
    def __new__(meta, name, bases, dct):
        # Construct the class
        res = super(ModuleMeta, meta).__new__(meta, name, bases, dct)

        # Wrap enable event signals
        res.enable = meta.signals_wrapper(res.enable, res, pre_enable, post_enable)
        res.disable = meta.signals_wrapper(res.disable, res, pre_disable, post_disable)
        return res

    @classmethod
    def signals_wrapper(cls, operation, new_class, pre, post):
        """
        Calls given pre and post signals with the given operation in between
        """
        def _wrapped(self, *args, **kwargs):
            # avoid double wrapping because of inheritance
            wrap = type(self) == new_class

            if wrap: pre.send(sender=self)
            res = operation(self, *args, **kwargs)
            if wrap: post.send(sender=self)
            return res

        return _wrapped

@receiver(post_enable)
def after_enable(sender, **kwargs):
    sender._info.status = ModuleInfo.ENABLED
    sender._info.save()

@receiver(post_disable)
def after_disable(sender, **kwargs):
    sender._info.status = ModuleInfo.DISABLED
    sender._info.save()


class Module(object):
    """
    NAZS module, implements everything needed to provide a feature.

    Module lifecycle
    ----------------

    Modules have 3 status: installed, enabled and disabled

    A module starts with installed status, if the user enables it,
    enable method will be called and the module will move to enabled status.

    After first enable the module can be switched between enabled or disabled,
    but cannot move to installed anymore.


    TODO

    Definitions
    -----------
       - pre init models
       - models
       - conf files
       - daemons
       - events

       MORE:
       - firewall helper
       - log files
       - cron
       - tasks

    Modules inter communication
       - signal on event

    """
    __metaclass__ = ModuleMeta

    def __init__(self):
        super(Module, self).__init__()
        name = self.__class__.__module__ + '.' + self.__class__.__name__
        self._info, _ = ModuleInfo.objects.get_or_create(name=name)

    @property
    def was_enabled(self):
        """
        Returns True if the module has been enabled some time before

        This tells if enable method has been called, it will be called only once.
        """
        return self._info.status > ModuleInfo.INSTALLED

    @property
    def enabled(self):
        """
        Tells if the module is currently enabled or disabled
        """
        return self._info.status == ModuleInfo.ENABLED

    @property
    def changed(self):
        """
        Tells if module configuration has been changed (and it needs to be saved)
        """
        return self._info.changed



    def enable(self):
        """
        Do the needed actions to enable this module
        """
        pass


    def disable(self):
        """
        Do the needed actions to disable this module
        """
        pass




