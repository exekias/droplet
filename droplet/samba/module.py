from droplet import module
from droplet.files import TemplateConfFile
from droplet.daemons import InitDaemon
from droplet.commands import run
from droplet.sudo import root
from droplet.interfaces.samba import ISambaServer
from droplet.util import make_password

import os
import shutil
import logging

from .models import DomainSettings


logger = logging.getLogger(__name__)


class Samba(module.Module, ISambaServer):
    """
    Samba 4 module, it deploys samba AD and file server
    """
    install_wizard = 'samba:install'

    SMBCONF_FILE = '/etc/samba/smb.conf'
    SMB_PRIVATE_DIR = '/var/lib/samba/private'
    KRB5CONF_FILE = '/etc/krb5.conf'
    SMB_KRB5CONF_FILE = os.path.join(SMB_PRIVATE_DIR, 'krb5.conf')

    # Conf files
    smbconf = TemplateConfFile(SMBCONF_FILE,
                               template='smb.conf',
                               template_params=lambda: {
                                   'settings': DomainSettings.get()
                               })

    # Daemons
    nmbd = InitDaemon('nmbd')
    smbd = InitDaemon('smbd')
    samba_ad = InitDaemon('samba-ad-dc')

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
                domain_settings.adminpass = make_password(15)
                domain_settings.save()

                run("samba-tool domain provision "
                    "--domain='%s' "
                    "--workgroup='%s' "
                    "--realm='%s' "
                    "--use-xattrs=yes "
                    "--use-rfc2307 "
                    "--server-role='domain controller' "
                    "--use-ntvfs "
                    "--adminpass='%s'" %
                    (domain_settings.domain,
                     domain_settings.workgroup,
                     domain_settings.realm,
                     domain_settings.adminpass))

                self.smbconf.write()

                shutil.copy2(self.SMB_KRB5CONF_FILE, self.KRB5CONF_FILE)

                # XXX FIXME move this to network
                run("echo 'nameserver 127.0.0.1' > /etc/resolv.conf")
                # TODO manage shares
                run("touch /etc/samba/shares.conf")

            elif domain_settings.mode == 'member':
                # TODO
                pass

    def save(self):

        # Save con files
        self.smbconf.write()

        with root():
            shutil.copy2(self.SMB_KRB5CONF_FILE, self.KRB5CONF_FILE)
            # XXX FIXME move this to network
            run("echo 'nameserver 127.0.0.1' > /etc/resolv.conf")

    def stop_other_daemons(self):
        """
        Stop services already provided by main samba daemon
        """
        if self.smbd.running:
            self.smbd.stop()

        if self.nmbd.running:
            self.nmbd.stop()

    def start(self):
        self.stop_other_daemons()
        self.samba_ad.start()

    def stop(self):
        self.stop_other_daemons()
        self.samba_ad.stop()

    def restart(self):
        self.stop_other_daemons()
        self.samba_ad.restart()

    def connection_info(self):
        domain_settings = DomainSettings.get()
        base_dn = 'dc=' + ',dc='.join(domain_settings.realm.split('.'))

        return {
            'host': '127.0.0.1',
            'bind_dn': 'cn=Administrator,cn=Users,%s' % base_dn,
            'bind_password': domain_settings.adminpass,
            'base_dn': base_dn,
            'protocol': 'ldap'
        }
