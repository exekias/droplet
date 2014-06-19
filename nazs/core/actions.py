from django.core.urlresolvers import reverse

from nazs.web import redirect
from nazs.actions import Library
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


@register.action
def enable_module(transport, table, module):
    module.enable()


@register.action
def disable_module(transport, table, module):
    module.disable()


@register.action
def apply_changes(transport):
    save()
