from nazs import Module
from nazs.files import TemplateConfFile

from models import Interfaces

class NetworkModule(Module):

    # Configuration files

    # Interfaces
    interfaces = TemplateConfFile('/etc/network/interfaces',
                                  template='interfaces',
                                  template_params=Interfaces.objects.all())

