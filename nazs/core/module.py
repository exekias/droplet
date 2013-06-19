from services import Service
from models import ModuleInfo


class Module(object):
    """
    NAZS module, implements everything needed to provide a feature.

    TODO

    Module lifecycle?
       - disabled
       <- enable
       + enable
       - enabled
       - set_conf
       - restart | reload

    Definitions
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
    def __init__(self):
        self._info = ModuleInfo.objects.get_or_create(self.name)


    def is_installed(self):
        return self._info.status > ModuleInfo.INSTALLED

    def is_enabled(self):
        return self._info.status == ModuleInfo.ENABLED


