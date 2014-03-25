from django.utils.translation import ugettext as _
from achilles import blocks, tables

from models import Interface

register = blocks.Library('network')


@register.block('interfaces')
class Interfaces(tables.Table):

    model = Interface

    name = tables.Column(verbose_name=_('Name'))

    configured = tables.Column(verbose_name=_('Configured'))
