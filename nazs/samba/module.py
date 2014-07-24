from nazs import module
from nazs.files import TemplateConfFile
from nazs.commands import run
from nazs.sudo import root

import os
import shutil
import logging

from .models import DomainSettings


logger = logging.getLogger(__name__)


class Samba(module.Module):
    """
    Samba 4 module, it deploys samba AD and file server
    """

    install_wizard = 'samba:install'

    SMBCONF_FILE = '/etc/samba/smb.conf'
    SMB_PRIVATE_DIR = '/var/lib/samba/private'
    KRB5CONF_FILE = '/etc/krb5.conf'
    SMB_KRB5CONF_FILE = os.path.join(SMB_PRIVATE_DIR, 'krb5.conf')

    smbconf = TemplateConfFile(SMBCONF_FILE,
                               template='smb.conf',
                               template_params=lambda: {
                                   'settings': DomainSettings.get()
                               })

    def install(self):
        """
        Installation procedure, it writes basic smb.conf and uses samba-tool to
        provision the domain
        """
        domain_settings = DomainSettings.get()

        with root():
            if os.path.exists(self.SMBCONF_FILE):
                os.remove(self.SMBCONF_FILE)

            if domain_settings.mode == 'ad':
                run("samba-tool domain provision "
                    "--domain='%s' "
                    "--workgroup='%s' "
                    "--realm='%s' "
                    "--use-xattrs=yes "
                    "--use-rfc2307 "
                    "--server-role='domain controller' "
                    "--use-ntvfs "
                    "--adminpass='foobar1!'" %
                    (domain_settings.domain,
                     domain_settings.workgroup,
                     domain_settings.realm))

                self.smbconf.write()

                shutil.copy2(self.SMB_KRB5CONF_FILE, self.KRB5CONF_FILE)

                ### XXX FIXME move this to network
                run("echo 'nameserver 127.0.0.1' > /etc/resolv.conf")
                ### TODO manage shares
                run("touch /etc/samba/shares.conf")

            elif domain_settings.mode == 'member':
                # TODO
                pass

    def save(self):

        with root():
            self.smbconf.write()

            shutil.copy2(self.SMB_KRB5CONF_FILE, self.KRB5CONF_FILE)

            ### XXX FIXME move this to network
            run("echo 'nameserver 127.0.0.1' > /etc/resolv.conf")

    def start(self):
        with root():
            run('service smbd stop')
            run('service nmbd stop')
            run('service samba-ad-dc start')

    def stop(self):
        with root():
            run('service smbd stop')
            run('service nmbd stop')
            run('service samba-ad-dc stop')

    def restart(self):
        with root():
            run('service smbd stop')
            run('service nmbd stop')
            run('service samba-ad-dc restart')
