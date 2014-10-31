# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.urlresolvers import reverse

import droplet

from droplet import actions
from droplet.web import blocks, forms, redirect


aregister = actions.Library('wizard')


class Wizard(blocks.Block):
    """
    Wizard block, it walks the user trough different forms (see
    class:`droplet.web.forms.FormBlock`)
    """
    template_name = 'web/wizard.html'

    #: Sorted list of class:`droplet.web.forms.Form` objects
    forms = []

    #: current step
    step = 0

    def get_forms(self):
        """
        Return the sorted list of forms of the wizard
        """
        return self.forms

    def get_context_data(self, *args, **kwargs):
        context = super(Wizard, self).get_context_data(*args, **kwargs)
        context.update({
            'wizard_name': self.register_name,
            'form_name': self.next(self.step).register_name,
            'step': self.step,
        })
        return context

    def next(self, step):
        forms = self.get_forms()
        return forms[step]


class InstallWizard(Wizard):
    """
    Wizard bounded to a module, it will install the module when done and
    redirect the user to moudles page
    """
    #: Class of the module this wizard will install
    module = None

    def __init__(self, *args, **kwargs):
        if not self.module or \
           not issubclass(self.module, droplet.module.Module):
            raise ValueError('You should define module class to be installed')

        super(InstallWizard, self).__init__(*args, **kwargs)

    def finish(self, transport):
        mod = self.module()
        mod.install()
        mod.enable()
        redirect.redirect(transport, reverse('core:modules'))


@aregister.action
def next(transport, wizard, step, data):
    """
    Validate step and go to the next one (or finish the wizard)

    :param transport: Transport object
    :param wizard: Wizard block name
    :param step: Current step number
    :param data: form data for the step
    """
    step = int(step)
    wizard = blocks.get(wizard)

    # Retrieve form block
    form = wizard.next(step)

    valid = forms.send(transport, form.register_name, data=data)

    if valid:
        if wizard.next(step+1) is None:
            # It was last step
            wizard.finish(transport)
            return

        # Next step
        wizard.step = step+1
        wizard.update(transport)
