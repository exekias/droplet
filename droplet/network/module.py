from droplet import module
from droplet.files import TemplateConfFile
from droplet.commands import run
from droplet.sudo import root

from .models import Interface

import logging


logger = logging.getLogger(__name__)


class Network(module.Module):

    # Configuration files

    interfaces = TemplateConfFile('/etc/network/interfaces',
                                  template='interfaces',
                                  template_params=lambda: {
                                      'interfaces': Interface.objects.all()
                                  })

    def start(self):
        for iface in Interface.objects.all():
            if not iface.configured:
                logger.debug("%s is not configured" % iface.name)
                continue

            with root():
                # we run ifup in background
                # it can wait indefinitely for DHCP requests
                run('/sbin/ifup --force %s' % iface.name, background=True)

    def stop(self):
        for iface in Interface.objects.all():
            if not iface.configured:
                logger.debug("%s is not configured" % iface.name)
                continue

            with root():
                run('/sbin/ifdown --force %s' % iface.name)
