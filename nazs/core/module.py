from django.dispatch import receiver

from services import Service
from models import ModuleInfo
from signals import pre_enable, post_enable, \
                    pre_disable, post_disable


class ModuleMeta(type):
    """
    Module metaclass, to allow some black magic tricks on module definitions
    """
    # Modules instances
    MODULES = {}

    def __new__(meta, name, bases, dct):
        # Construct the class
        cls = super(ModuleMeta, meta).__new__(meta, name, bases, dct)

        # Wrap enable event signals
        cls.enable = meta.enable_wrapper(cls.enable, cls)
        cls.disable = meta.disable_wrapper(cls.disable, cls)

        if cls not in ModuleMeta.MODULES:
            ModuleMeta.MODULES[cls] = None
        return cls

    def __call__(cls, *args, **kw):
        if cls not in ModuleMeta.MODULES or ModuleMeta.MODULES[cls] is None:
            ModuleMeta.MODULES[cls] = super(ModuleMeta, cls).__call__(*args, **kw)
        return ModuleMeta.MODULES[cls]

    @classmethod
    def enable_wrapper(cls, enable, new_class):
        """
        Wrap the enable method to call pre and post enable signals and update
        module status
        """
        def _wrapped(self, *args, **kwargs):
            # avoid double wrapping because of inheritance
#            wrap = type(self) == new_class
#            if not wrap:
#                return enable(self, *args, **kwargs)

            if self.enabled:
                raise AssertionError('Module %s is already enabled' % self.name)

            if not self.was_enabled:
                self.first_enable()

            pre_enable.send(sender=self)
            res = enable(self, *args, **kwargs)
            post_enable.send(sender=self)

            self._info.status = ModuleInfo.ENABLED
            self._info.save()
            return res

        return _wrapped

    @classmethod
    def disable_wrapper(cls, disable, new_class):
        """
        Wrap the disable method to call pre and post disable signals and update
        module status
        """
        def _wrapped(self, *args, **kwargs):
            if not self.enabled:
                raise AssertionError('Module %s is already disabled' % self.name)

            pre_disable.send(sender=self)
            res = disable(self, *args, **kwargs)
            post_disable.send(sender=self)

            self._info.status = ModuleInfo.DISABLED
            self._info.save()
            return res

        return _wrapped


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
    def name(self):
        """
        Return the user visible name of the module
        """
        return self.__class__.__name__

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


    def first_enable(self):
        """
        First enable actions, called only the first time the module is enabled
        """
        pass

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




