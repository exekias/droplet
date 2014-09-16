from django import forms

from .models import Module, Conf


class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module


class ConfForm(forms.ModelForm):

    class Meta:
        model = Conf
