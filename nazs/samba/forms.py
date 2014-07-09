from django import forms

from .models import DomainSettings


class DomainSettingsForm(forms.ModelForm):

    class Meta:
        model = DomainSettings
