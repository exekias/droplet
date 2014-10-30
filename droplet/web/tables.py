# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _
from achilles.tables import *  # noqa
from achilles import actions, blocks, forms


bregister = blocks.Library('droplet')
aregister = actions.Library('droplet')


# OBJECT EDIT COLUMN


@bregister.block(name='edit')
class EditColumnBlock(forms.Form):

    template_name = 'web/form_edit.html'

    save = forms.SubmitButton(verbose_name=_('Save'))

    cancel = forms.ResetButton(verbose_name=_('Cancel'))

    def get_form(self, form_data=None, table_name=None,
                 column_name=None, obj_id=None, **kwargs):
        table = blocks.get(table_name)
        column = getattr(table, column_name)
        self.form_class = column.form_class
        return super(EditColumnBlock, self).get_form(form_data=form_data,
                                                     table_name=table_name,
                                                     column_name=column_name,
                                                     obj_id=obj_id,
                                                     **kwargs)

    def get_instance(self, table_name, column_name, obj_id, *args, **kwargs):
        table = blocks.get(table_name)
        return table.get_object(obj_id)

    def get_context_data(self, table_name=None,
                         column_name=None, obj_id=None, *args, **kwargs):
        context = super(EditColumnBlock, self).get_context_data(
            table_name=table_name,
            column_name=column_name,
            obj_id=obj_id,
            **kwargs)
        context['table_name'] = table_name
        return context

    def form_valid(self, transport, form, table_name=None,
                   column_name=None, obj_id=None):

        # Save the form
        form.save()

        # Update the table
        blocks.update(transport, table_name)


@bregister.block(name='create')
class CreateColumnBlock(EditColumnBlock):

    def get_instance(self, table_name, column_name, *args, **kwargs):
        return None


class EditColumn(ButtonColumn):
    """
    Action to show a form for the given object
    """
    def __init__(self, form_class, classes='btn btn-primary',
                 verbose_name=_('Edit'), **kwargs):
        super(EditColumn, self).__init__(classes=classes,
                                         verbose_name=verbose_name,
                                         **kwargs)
        self.form_class = form_class

    def get_href(self, obj):
        return ("javascript:achilles.loadInto(achilles.block('%s')"
                ".find('.pretable'), 'droplet:edit', ['%s', '%s', '%s'])") % \
               (self.table.register_name, self.table.register_name,
                self.name, self.table.get_object_id(obj))


@aregister.action('delete')
def delete(transport, table, obj):
    obj.delete()
    blocks.update(transport, table.register_name)


class DeleteColumn(ActionColumn):
    """
    Action to delete an item
    """
    def __init__(self, classes='btn btn-danger', verbose_name=_('Delete'),
                 **kwargs):
        super(DeleteColumn, self).__init__(delete, classes=classes,
                                           verbose_name=verbose_name,
                                           **kwargs)


# TABLE ACTIONS

class TableAction(object):
    """
    Table action, executes an action on the whole table
    """
    creation_counter = 0

    def __init__(self, action, verbose_name=None, visible=lambda x: True,
                 classes='btn btn-default'):
        """
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        :param visible: Function giving visibility flag for the given row
        :param action: Action to call
        :param classes: CSS classes to apply to the button
        """
        TableAction.creation_counter += 1
        self.creation_counter = TableAction.creation_counter
        self.verbose_name = verbose_name
        self.visible = visible
        self.action = action
        self.classes = classes

    def contribute_to_class(self, table, name):
        self.name = name
        self.verbose_name = self.verbose_name or name
        self.table = table

    def render(self):
        """
        Render table action button
        """
        if self.visible(self.table):
            return self.content()
        else:
            return ''

    def get_href(self):
        return ("javascript:achilles.action('web:table_action',"
                "['%s', '%s'])") % (self.table.register_name, self.name)

    def content(self):
        return '<a href="%s" class="%s">%s</a>' % \
               (self.get_href(), self.classes, self.verbose_name)

    def call(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class AddAction(TableAction):
    """
    Table object add action, show the given form to create a new item
    in the table
    """
    def __init__(self, form_class, verbose_name=_('Add'), *args, **kwargs):
        super(AddAction, self).__init__(None, *args, verbose_name=verbose_name,
                                        **kwargs)
        self.form_class = form_class

    def get_href(self):
        return ("javascript:achilles.loadInto(achilles.block('%s')"
                ".find('.pretable'), 'droplet:create', ['%s', '%s'])") % \
               (self.table.register_name, self.table.register_name, self.name)


# TABLE CLASS OVERRIDES


class Table(Table):
    # Override table template
    Table.template_name = 'web/table.html'

    def actions(self):
        """
        List of :class:`TableAction` elements defined for this table
        """
        actions = []
        for a in dir(self):
            a = getattr(self, a)
            if isinstance(a, TableAction):
                actions.append(a)

        # We are not caching this because array len should be low enough
        actions.sort(key=lambda action: action.creation_counter)
        return actions
