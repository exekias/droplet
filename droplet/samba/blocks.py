from droplet.web import blocks, forms, wizards

from .forms import DomainSettingsForm
from .module import Samba


register = blocks.Library('samba')


@register.block
class DomainSettings(forms.ModelForm):
    form_class = DomainSettingsForm


@register.block(name='install')
class InstallSamba(wizards.InstallWizard):
    module = Samba
    forms = [DomainSettings, ]
