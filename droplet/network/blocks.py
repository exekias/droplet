from django.utils.translation import ugettext as _
from droplet.web import tables, blocks

from .forms import InterfaceForm
from .models import Interface

register = blocks.Library('network')


@register.block('interfaces')
class Interfaces(tables.Table):

    model = Interface

    name = tables.Column(verbose_name=_('Name'))

    configured = tables.Column(verbose_name=_('Configured'))

    edit = tables.EditColumn(InterfaceForm, verbose_name=_('Edit'))
