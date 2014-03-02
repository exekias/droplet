import logging

from django.db.models import get_app, get_models

from .models import ModuleInfo
from .files import ConfFile
from .signals import (pre_install, post_install,
                      pre_enable, post_enable,
                      pre_disable, post_disable,
                      pre_save, post_save)


logger = logging.getLogger(__name__)


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

            logger.info("Installing %s module" % self.name)
            pre_install.send(sender=self)
            res = install(self, *args, **kwargs)
            post_install.send(sender=self)

            info = self._info
            info.status = ModuleInfo.DISABLED
            info.save()

            logger.info("Installed %s module" % self.name)
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

            logger.info("Enabling %s module" % self.name)
            pre_enable.send(sender=self)
            res = enable(self, *args, **kwargs)
            post_enable.send(sender=self)

            info = self._info
            info.status = ModuleInfo.ENABLED
            info.save()

            logger.info("Enabled %s module" % self.name)
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

            logger.info("Saving % module" % self.name)
            pre_save.send(sender=self)
            res = save(self, *args, **kwargs)
            post_save.send(sender=self)
            logger.info("Saved % module" % self.name)

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

            logger.info("Disabling %s module" % self.name)
            pre_disable.send(sender=self)
            res = disable(self, *args, **kwargs)
            post_disable.send(sender=self)

            info = self._info
            info.status = ModuleInfo.DISABLED
            info.save()

            logger.info("Disabled %s module" % self.name)
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

    After installing the module, it can be switched between enabled or
    disabled, but cannot move to not installed anymore. See enable() and
    disable() methods.

    When the configuration for a module has changed and the user ask to apply
    it, the save() method will be called. This will write all configuration
    needed to make the module work.

    Depending on the status of the module, the system will call 3 different
    methods to operate it: start(), stop() or restart().


    Module status          Running status

    - FIRST CONFIGURATION
    not installed             stopped
       |--install()              |
    disabled                     |
       |--enable()               |
    enabled                      |
       |--save()                 |
       |--start()                |
                              running

    - CONF CHANGE
    enabled                   running
      |--save()                  |
      |--restart()               ~
                              running

    - BOOT
    enabled                   stopped
       |--start()                |
                              running

    - DISABLE
    enabled                   running
       |--stop()                 |
       |--disable()           stopped
    disabled

    TODO

    Definitions
    -----------
       - pre install models
       - models
       - daemons
       - events

       MORE:
       - firewall helper
       - log files
       - cron
       - tasks

    Modules inter communication
       - signal on event
       - providers

    """
    __metaclass__ = ModuleMeta

    def __init__(self):
        super(Module, self).__init__()

    @property
    def _info(self):
        """
        Module internal status representation
        """
        name = self.__class__.__module__ + '.' + self.__class__.__name__
        info, created = ModuleInfo.objects.get_or_create(name=name)
        if created:
            # Do not set as changed
            info.commit()
        return info

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
        # Not installed modules cannot issue a change to save
        if not self.installed:
            return False

        # Check if module status changed
        if self._info._changed:
            return True

        # Check model changes
        for model in self.models():
            if model.objects.changed().count():
                return True

        # Nothing passed, module not changed
        return False

    def commit(self):
        """
        Commit changes in all the models for this module. This method is call
        after applying changes, unmarking changed/new rows and deleting purging
        objects
        """
        for model in self.models():
            model.commit()

    def models(self):
        """
        Return all the models defined for this module
        """
        app = get_app(self.__class__.__module__.split('.')[-2])
        return get_models(app)

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
        Do the needed actions to enable this module. You can assume that
        install was called before
        """
        pass

    def disable(self):
        """
        Do the needed actions to disable this module
        """
        pass

    # Save changes

    def save(self):
        """
        Write config needed to make this module work. By default it ensures
        that all conf files are written

        If you need more advanced stuff you can override this method
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

    # Start / stop

    def start(self):
        """
        Start running the module (start daemons, launch services...)
        """
        pass

    def stop(self):
        """
        Stop module from running (stop daemons)
        """
        pass

    def restart(self):
        """
        Restart module
        """
        self.stop()
        self.start()
