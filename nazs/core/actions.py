from achilles import blocks, actions

import nazs


register = actions.Library('core')


@register.action
def install_module(request, table, module):
    module.install()
    module.enable()
    blocks.update(request, 'core:menu')
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
    nazs.save()


def update_save_button(request, **kwargs):
    blocks.update(request, 'core:apply_button')


actions.post_actions_call.connect(update_save_button)
