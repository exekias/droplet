from django.utils.translation import ugettext as _
from django.dispatch import receiver

from nazs.actions import post_action_call, post_actions_call
from nazs.web import blocks, tables, menus
from ..actions import install_module

import nazs

register = blocks.Library('core')


def update_save_button(transport, **kwargs):
    blocks.update(transport, 'core:apply_button')


# Always update save button
post_actions_call.connect(update_save_button)


@register.block(template_name='web/core/welcome.html')
def home():
    return {'version': nazs.__version__}


@register.block(template_name='web/core/menu.html')
def menu():
    return {'menu': menus.menu()}


@receiver(post_action_call, sender=install_module)
def process_menu_change(sender, transport, **kwargs):
    blocks.update(transport, 'core:menu')


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
