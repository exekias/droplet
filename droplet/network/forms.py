from django import forms

from .models import Interface


class InterfaceForm(forms.ModelForm):

    class Meta:
        model = Interface
