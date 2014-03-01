from django.utils.translation import ugettext as _
from achilles import blocks, tables

import nazs

register = blocks.Library('core')


@register.block(template_name='web/core/welcome.html')
def home():
    return {'version': nazs.__version__}


@register.block('modules')
class Modules(tables.Table):

    id_field = 'name'

    # Module name
    name = tables.Column(verbose_name=_('Module'))

    # Module status
    status = tables.MergeColumn(
        verbose_name=_('Status'),
        columns=(
            ('install', tables.ActionColumn(verbose_name='Install',
                                            action='core:install_module',
                                            visible=lambda m: not m.installed)),

            ('enable', tables.ActionColumn(verbose_name='Enable',
                                           action='core:enable_module',
                                           visible=lambda m: m.installed and
                                           not m.enabled)),

            ('disable', tables.ActionColumn(verbose_name='Enable',
                                            action='core:disable_module',
                                            visible=lambda m: m.installed and
                                            m.enabled)),
        )
    )

    def objects(self):
        return nazs.modules()
