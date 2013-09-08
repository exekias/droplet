from django.dispatch import receiver

from models import ModuleInfo
from files import ConfFile
from signals import (pre_install, post_install,
                     pre_enable, post_enable,
                     pre_disable, post_disable,
                     pre_save, post_save)


class ModuleMeta(type):
    """
    Module metaclass, to allow some black magic tricks on module definitions
    """
    # Modules instances
    MODULES = {}

    def __new__(meta, name, bases, dct):
        # Construct the class
        cls = super(ModuleMeta, meta).__new__(meta, name, bases, dct)

        # Ignore base class
        if object in bases:
            return cls

        # Wrap enable event signals
        cls.install = meta.install_wrapper(cls.install, cls)
        cls.enable = meta.enable_wrapper(cls.enable, cls)
        cls.disable = meta.disable_wrapper(cls.disable, cls)
        cls.save = meta.save_wrapper(cls.save, cls)

        if cls not in ModuleMeta.MODULES:
            ModuleMeta.MODULES[cls] = None
        return cls

    def __call__(cls, *args, **kw):
        if cls not in ModuleMeta.MODULES or ModuleMeta.MODULES[cls] is None:
            ModuleMeta.MODULES[cls] = \
                super(ModuleMeta, cls).__call__(*args, **kw)
        return ModuleMeta.MODULES[cls]

    @classmethod
    def install_wrapper(cls, install, new_class):
        """
        Wrap the install method to call pre and post enable signals and update
        module status
        """
        def _wrapped(self, *args, **kwargs):
            if self.installed:
                raise AssertionError('Module %s is already installed'
                                     % self.name)

            pre_install.send(sender=self)
            res = install(self, *args, **kwargs)
            post_install.send(sender=self)

            self._info.status = ModuleInfo.DISABLED
            self._info.save()
            return res

        return _wrapped

    @classmethod
    def enable_wrapper(cls, enable, new_class):
        """
        Wrap the enable method to call pre and post enable signals and update
        module status
        """
        def _wrapped(self, *args, **kwargs):
            if not self.installed:
                raise AssertionError('Module %s cannot be enabled'
                                     ', you should install it first'
                                     % self.name)

            if self.enabled:
                raise AssertionError('Module %s is already enabled'
                                     % self.name)

            pre_enable.send(sender=self)
            res = enable(self, *args, **kwargs)
            post_enable.send(sender=self)

            self._info.status = ModuleInfo.ENABLED
            self._info.save()
            return res

        return _wrapped

    @classmethod
    def save_wrapper(cls, save, new_class):
        """
        Wrap the save method to call pre and post enable signals and update
        module status
        """
        def _wrapped(self, *args, **kwargs):
            if not self.installed:
                raise AssertionError('Module %s is not installed' % self.name)

            pre_save.send(sender=self)
            res = save(self, *args, **kwargs)
            post_save.send(sender=self)

            self._info.commit_save()  # TODO commit_save all module models
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
                raise AssertionError('Module %s is already disabled'
                                     % self.name)

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

    Modules have 3 status: not installed, enabled and disabled

    A module starts with not installed status, if the user installs it,
    install() method will be called and the module will move to disabled status

    After install the module can be switched between enabled or disabled,
    but cannot move to not installed anymore.


    TODO

    Definitions
    -----------
       - pre install models
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

    # Status info

    @property
    def installed(self):
        """
        Returns True if the module has been installed
        """
        return self._info.status > ModuleInfo.NOT_INSTALLED

    @property
    def enabled(self):
        """
        Tells if the module is currently enabled or disabled
        """
        return self._info.status == ModuleInfo.ENABLED

    @property
    def changed(self):
        """
        Tells if module configuration has been changed (it needs to be saved)
        """
        return self._info.changed

    # Enable / disable actions

    def install(self):
        """
        Setup actions, called only once. This method should assume nothing
        about the status of the system before, but leave it
        ready to enable and start using the module
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

    # Save changes process

    def save(self):
        """
        Apply module changes to the system, it will basically:

         - Call write_conf()
         - Call manage_daemons()

        If you need more advanced stuff you can override thiss method
        """
        self.write_conf()
        self.manage_daemons()

    def write_conf(self):
        """
        Write configuration files for this module
        """
        for f in self.conf_files():
            f.write()

    def conf_files(self):
        """
        List of configuration files for this module
        """
        for attr in dir(self):
            field = getattr(self, attr)
            if isinstance(field, ConfFile):
                yield field

    def manage_daemons(self):
        """
        Write configuration files for this module
        """
        pass
