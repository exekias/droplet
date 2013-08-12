from nazs import Module
from nazs.files import TemplateConfFile

from models import Interface


class Network(Module):

    # Configuration files

    interfaces = TemplateConfFile('/etc/network/interfaces',
                                  template='interfaces',
                                  template_params={
                                      'interfaces': Interface.objects.all()
                                  })