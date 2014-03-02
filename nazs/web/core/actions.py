from nazs import actions, blocks


register = actions.Library('core')


@register.action
def install_module(request, module):
    module.install()
    blocks.update(request, 'core:modules')

@register.action
def enable_module(request, module):
    module.enable()
    blocks.update(request, 'core:modules')

@register.action
def disable_module(request, module):
    module.disable()
    blocks.update(request, 'core:modules')
