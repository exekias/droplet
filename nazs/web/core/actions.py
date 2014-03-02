from achilles import blocks, actions


register = actions.Library('core')


@register.action
def install_module(request, table, module):
    module.install()
    blocks.update(request, table.register_name)

@register.action
def enable_module(request, table, module):
    module.enable()
    blocks.update(request, table.register_name)

@register.action
def disable_module(request, table, module):
    module.disable()
    blocks.update(request, table.register_name)

def update_save_button(request, **kwargs):
    blocks.update(request, 'core:save_button')

actions.post_actions_call.connect(update_save_button)
