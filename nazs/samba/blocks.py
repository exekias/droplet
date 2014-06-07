from achilles import blocks, forms
from nazs.core.wizards import InstallWizard

from .forms import Mode
from .module import Samba


register = blocks.Library('samba')


@register.block
class mode(forms.FormBlock):
    form_class = Mode

    def form_valid(self, request, form):
        pass


@register.block(name='install')
class InstallSamba(InstallWizard):
    module = Samba
    forms = [mode, ]
