from nazs.core import module
from nazs.core.commands import run
from nazs.core.sudo import root

from django.utils.translation import ugettext as _

import os
import logging


logger = logging.getLogger(__name__)


class Samba(module.Module):
    """
    Samba 4 module, it deploys samba AD and file server
    """
    ETC_FILE = '/etc/samba/smb.conf'

    def install(self):
        """
        Installation procedure, it writes basic smb.conf and uses samba-tool to
        provision the domain
        """
        with root():
            if os.path.exists(self.ETC_FILE):
                os.unlink(self.ETC_FILE)

            run("samba-tool domain provision "
                " --domain='zentyal' "
                " --workgroup='zentyal' "
                "--realm='zentyal.lan' "
                "--use-xattrs=yes "
                "--use-rfc2307 "
                "--server-role='domain controller' "
                "--use-ntvfs "
                "--adminpass='foobar1!'")

    def menu(self):
        menu = module.MenuItem('samba', verbose_name=_('Directory'))
        menu.append(module.MenuItem('interfaces',
                                    'http://google.com',
                                    verbose_name=_('Interfaces')))

        return (menu,)
