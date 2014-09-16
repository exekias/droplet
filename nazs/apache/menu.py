from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from nazs.web.menus import MenuItem


def menu(root):
    apache = MenuItem('apache', verbose_name=_('Apache'))

    apache.append(MenuItem('modules', reverse('apache:modules'),
                           verbose_name=_('Modules')))

    apache.append(MenuItem('confs', reverse('apache:confs'),
                           verbose_name=_('Configurations')))

    root.append(apache)
