from achilles import blocks


class Wizard(blocks.Block):
    """
    Wizard block, it walks the user trough different forms (see
    class:`achilles.forms.Form`)
    """
    template_name = 'web/wizard.html'

    #: Sorted list of class:`achilles.forms.Form` objects
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
