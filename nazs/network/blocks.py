from django.utils.translation import ugettext as _
from nazs.web import tables, blocks, forms

from .forms import InterfaceForm
from .models import Interface

register = blocks.Library('network')


@register.block('interfaces')
class Interfaces(tables.Table):

    model = Interface

    name = tables.Column(verbose_name=_('Name'))

    configured = tables.Column(verbose_name=_('Configured'))

    edit = tables.EditColumn('network:edit_interface', verbose_name=_('Edit'))


# TODO update interfaces block after save
@register.block('edit_interface')
class EditInterface(forms.ModelFormBlock):
    form_class = InterfaceForm
