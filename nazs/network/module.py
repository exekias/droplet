from nazs.core.module import Module
from nazs.core.files import TemplateConfFile
from nazs.core.commands import run
from nazs.core.sudo import root

from models import Interface


class Network(Module):

    # Configuration files

    interfaces = TemplateConfFile('/etc/network/interfaces',
                                  template='interfaces',
                                  template_params=lambda: {
                                      'interfaces': Interface.objects.all()
                                  })

    def start(self):
        for iface in Interface.objects.filter():
            if not iface.configured:
                continue

            with root():
                run('/sbin/ifup --force %s' % iface.name)

    def stop(self):
        for iface in Interface.objects.all():
            if not iface.configured:
                continue

            with root():
                run('/sbin/ifdown --force %s' % iface.name)
