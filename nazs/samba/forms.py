from django.utils.translation import ugettext as _
from django import forms


class Mode(forms.Form):

    CHOICES = (
        ('ad', _('Domain Controller')),
        ('member', _('Domain member')),
    )
    mode = forms.ChoiceField(choices=CHOICES)
