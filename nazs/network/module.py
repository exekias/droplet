from nazs.core.module import Module
from nazs.core.files import TemplateConfFile
from nazs.core.commands import run
from nazs.core.sudo import root

from nazs.network.models import Interface

import logging


logger = logging.getLogger(__name__)


class Network(Module):

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
