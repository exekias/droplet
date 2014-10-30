from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from droplet.web.menus import MenuItem


def menu(root):
    network = MenuItem('network', verbose_name=_('Network'))

    network.append(MenuItem('interfaces',
                            reverse('network:interfaces'),
                            verbose_name=_('Interfaces')))

    root.append(network)
