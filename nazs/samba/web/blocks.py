from nazs.web import blocks, forms, wizards

from ..forms import Mode
from ..module import Samba


register = blocks.Library('samba')


@register.block
class mode(forms.FormBlock):
    form_class = Mode
    save_button = False

    def form_valid(self, transport, form):
        pass


@register.block(name='install')
class InstallSamba(wizards.InstallWizard):
    module = Samba
    forms = [mode, ]
