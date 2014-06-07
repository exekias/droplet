from django import forms

from .models import Interface

import logging
logger = logging.getLogger(__name__)


class InterfaceForm(forms.ModelForm):

    class Meta:
        model = Interface
