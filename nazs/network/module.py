from nazs.core.module import Module
from nazs.core.files import TemplateConfFile

from models import Interface


class Network(Module):

    # Configuration files

    interfaces = TemplateConfFile('/etc/network/interfaces',
                                  template='interfaces',
                                  template_params=lambda: {
                                      'interfaces': Interface.objects.all()
                                  })
