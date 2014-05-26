from django.utils.translation import ugettext as _
from achilles import blocks, forms, tables
from nazs.web.tables import EditColumn

from .forms import InterfaceForm
from .models import Interface

register = blocks.Library('network')


@register.block('interfaces')
class Interfaces(tables.Table):

    model = Interface

    name = tables.Column(verbose_name=_('Name'))

    configured = tables.Column(verbose_name=_('Configured'))

    edit = EditColumn('network:edit_interface', verbose_name=_('Edit'))


@register.block('edit_interface')
class EditInterface(forms.Form):
    form_class = InterfaceForm
    template_name = 'web/form.html'

    def get_form(self, form_data=None, interface_id=None, *args, **kwargs):
        interface = None
        if interface_id:
            interface = Interface.objects.get(id=interface_id)
        return self.form_class(form_data, instance=interface)

    def form_valid(self, request, form):
        form.save()
        blocks.update(request, 'network:interfaces')
