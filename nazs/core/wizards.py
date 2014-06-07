from django.core.urlresolvers import reverse

import nazs
from nazs.web import blocks, actions, forms, redirect


aregister = actions.Library('wizard')


class Wizard(blocks.Block):
    """
    Wizard block, it walks the user trough different forms (see
    class:`nazs.web.forms.FormBlock`)
    """
    template_name = 'web/core/wizard.html'

    #: Sorted list of class:`nazs.web.forms.Form` objects
    forms = []

    #: current step
    step = 0

    def get_forms(self, *args, **kwargs):
        """
        Return the sorted list of forms of the wizard
        """
        return self.forms

    def get_context_data(self, *args, **kwargs):
        context = super(Wizard, self).get_context_data(*args, **kwargs)
        forms = self.get_forms(*args, **kwargs)
        context.update({
            'wizard_name': self.register_name,
            'form_name': forms[self.step].register_name,
            'step': self.step,
            'step_count': len(forms),
            'last': self.step == len(forms),
        })
        return context


class InstallWizard(Wizard):
    """
    Wizard bounded to a module, it will install the module when done and
    redirect the user to moudles page
    """
    #: Class of the module this wizard will install
    module = None

    def __init__(self, *args, **kwargs):
        if not self.module or \
           not issubclass(self.module, nazs.core.module.Module):
            raise ValueError('You should define module class to be installed')

        super(InstallWizard, self).__init__(*args, **kwargs)

    def finish(self, request):
        mod = self.module()
        mod.install()
        mod.enable()
        redirect.redirect(request, reverse('modules'))


@aregister.action
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

    valid = forms.send(request, form.register_name, data=data)

    if valid:
        if wizard.step+1 >= len(allforms):
            # It was last step
            wizard.finish(request)
            return

        # Next step
        wizard.step = step+1
        wizard.update(request)
