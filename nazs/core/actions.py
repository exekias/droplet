from django.core.urlresolvers import reverse

from .signals import menu_changed

from nazs.web import blocks, actions, redirect
from nazs import save


register = actions.Library('core')


@register.action
def install_module(request, table, module):

    # Go to wizard if module declares one
    if module.install_wizard:
        wizard_url = reverse('wizard', kwargs={'block': module.install_wizard})
        redirect.redirect(request, wizard_url)
        return

    module.install()
    module.enable()

    menu_changed.send(None, request=request)
    blocks.update(request, table.register_name)


@register.action
def enable_module(request, table, module):
    module.enable()
    blocks.update(request, table.register_name)


@register.action
def disable_module(request, table, module):
    module.disable()
    blocks.update(request, table.register_name)


@register.action
def apply_changes(request):
    save()


def update_save_button(request, **kwargs):
    blocks.update(request, 'core:apply_button')


# Always update save button
actions.post_actions_call.connect(update_save_button)
