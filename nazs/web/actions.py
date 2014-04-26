from achilles import blocks, actions, forms


register = actions.Library('web')


@register.action
def next(request, wizard, step, data):
    """
    Validate step and go to the next one (or finish the wizard)

    :param request: Request object
    :param wizard: Wizard block name
    :param step: Current step number
    :param data: form data for the step
    """
    step = int(step)
    wizard = blocks.get(wizard)
    allforms = wizard.get_forms()

    # Retrieve form block
    form = allforms[step]

    valid = forms.send(request, form.register_name, data)

    if valid:
        if wizard.step+1 >= len(allforms):
            # It was last step
            wizard.finish(request)
            return

        # Next step
        wizard.step = step+1
        wizard.update(request)
