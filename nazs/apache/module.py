from nazs import module
from nazs.daemons import InitDaemon
from nazs.sudo import root
from nazs.commands import run

import logging

from .models import Module, Conf

logger = logging.getLogger(__name__)


class Apache(module.Module):
    """
    Apache web server
    """
    # Conf files
#    smbconf = TemplateConfFile(SMBCONF_FILE,
#                               template='smb.conf',
#                               template_params=lambda: {
#                                   'settings': DomainSettings.get()
#                               })

    # Daemons
    apache2 = InitDaemon('apache2')

    def install(self):
        pass

    def save(self):
        super(Apache, self).save()

        # Manage special files
        with root():
            for mod in Module.objects.changed().filter(system=False):
                # FIXME just do a symbolink link?
                command = 'a2enmod' if mod.enabled else 'a2dismod'
                run('/usr/sbin/%s %s' % (command, mod.name))

            for conf in Conf.objects.changed().filter(system=False):
                command = 'a2enconf' if conf.enabled else 'a2disconf'
                run('/usr/sbin/%s %s' % (command, conf.name))
