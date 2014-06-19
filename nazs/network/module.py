from nazs import module
from nazs.files import TemplateConfFile
from nazs.commands import run
from nazs.sudo import root

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

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

    def menu(self, root):
        network = module.MenuItem('network', verbose_name=_('Network'))
        network.append(module.MenuItem('interfaces', reverse('interfaces'),
                                       verbose_name=_('Interfaces')))
        root.append(network)

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
