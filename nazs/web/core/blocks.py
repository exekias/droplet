from django.utils.translation import ugettext as _
from achilles import blocks, tables

import nazs

register = blocks.Library('core')


@register.block(template_name='web/core/welcome.html')
def home():
    return {'version': nazs.__version__}


def module_status(mod, field):
    if not mod.installed:
        return _('Not installed')

    if mod.enabled:
        return _('Disabled')
    else:
        return _('Enable')


@register.block('modules')
class Modules(tables.Table):

    id_field = 'name'

    # Module name
    name = tables.Column(verbose_name=_('Module'))

    # Module status
    status = tables.Column(verbose_name=_('Status'),
                           accessor=module_status)

    def objects(self):
        return nazs.modules()
