from django.utils.translation import ugettext as _
from achilles import blocks, tables

import nazs

register = blocks.Library('core')


@register.block(template_name='web/core/welcome.html')
def home():
    return {'version': nazs.__version__}


@register.block(template_name='web/core/apply_button.html')
def apply_button():
    return {'active': nazs.changed()}


@register.block('modules')
class Modules(tables.Table):

    id_field = 'name'

    # Module name
    name = tables.Column(verbose_name=_('Module'))

    # Module status
    status = tables.MergeColumn(
        verbose_name=_('Status'),
        columns=(
            ('install',
             tables.ActionColumn(verbose_name=_('Install'),
                                 action='core:install_module',
                                 classes='btn btn-primary',
                                 visible=lambda m: not m.installed)),

            ('enable',
             tables.ActionColumn(verbose_name=_('Enable'),
                                 action='core:enable_module',
                                 classes='btn btn-success',
                                 visible=lambda m: m.installed and
                                 not m.enabled)),

            ('disable',
             tables.ActionColumn(verbose_name=_('Disable'),
                                 action='core:disable_module',
                                 classes='btn btn-info',
                                 visible=lambda m: m.installed and
                                 m.enabled)),
        )
    )

    def objects(self):
        return nazs.modules()

    def get_object(self, name):
        for module in nazs.modules():
            if module.name == name:
                return module

        raise KeyError('Module %s not found' % name)
