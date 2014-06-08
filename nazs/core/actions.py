from django.core.urlresolvers import reverse
from achilles.actions import *

from .signals import menu_changed

from nazs.web import blocks, redirect
from nazs import save


register = Library('core')


@register.action
def install_module(transport, table, module):

    # Go to wizard if module declares one
    if module.install_wizard:
        wizard_url = reverse('wizard', kwargs={'block': module.install_wizard})
        redirect.redirect(transport, wizard_url)
        return

    module.install()
    module.enable()

    menu_changed.send(None, transport=transport)
    blocks.update(transport, table.register_name)


@register.action
def enable_module(transport, table, module):
    module.enable()
    blocks.update(transport, table.register_name)


@register.action
def disable_module(transport, table, module):
    module.disable()
    blocks.update(transport, table.register_name)


@register.action
def apply_changes(transport):
    save()


def update_save_button(transport, **kwargs):
    blocks.update(transport, 'core:apply_button')


# Always update save button
post_actions_call.connect(update_save_button)
