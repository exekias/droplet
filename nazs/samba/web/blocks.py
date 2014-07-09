from nazs.web import blocks, forms, wizards

from ..forms import DomainSettingsForm
from ..module import Samba


register = blocks.Library('samba')


@register.block
class DomainSettings(forms.ModelFormBlock):
    form_class = DomainSettingsForm
    save_button = False


@register.block(name='install')
class InstallSamba(wizards.InstallWizard):
    module = Samba
    forms = [DomainSettings, ]
