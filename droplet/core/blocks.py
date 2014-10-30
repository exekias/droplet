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

from django.utils.translation import ugettext as _
from django.dispatch import receiver

from droplet.actions import post_action_call, post_actions_call
from droplet.web import blocks, tables, menus
from .actions import install_module, enable_module, disable_module

import droplet

register = blocks.Library('core')


def update_save_button(transport, **kwargs):
    blocks.update(transport, 'core:apply_button')


# Always update save button
post_actions_call.connect(update_save_button)


@register.block(template_name='web/core/welcome.html')
def home():
    return {'version': droplet.__version__}


@register.block(template_name='web/core/menu.html')
def menu():
    return {'menu': menus.menu()}


@receiver(post_action_call, sender=install_module)
def process_menu_change(sender, transport, **kwargs):
    blocks.update(transport, 'core:menu')


@register.block(template_name='web/core/apply_button.html')
def apply_button():
    return {'active': droplet.changed()}


@register.block('modules')
class Modules(tables.Table):

    id_field = 'name'

    # Module name
    verbose_name = tables.Column(verbose_name=_('Module'))

    # Module status
    status = tables.MergeColumn(
        verbose_name=_('Status'),
        columns=(
            ('install',
             tables.ActionColumn(verbose_name=_('Install'),
                                 action=install_module,
                                 classes='btn btn-primary',
                                 visible=lambda m: not m.installed)),

            ('enable',
             tables.ActionColumn(verbose_name=_('Enable'),
                                 action=enable_module,
                                 classes='btn btn-success',
                                 visible=lambda m: m.installed and
                                 not m.enabled)),

            ('disable',
             tables.ActionColumn(verbose_name=_('Disable'),
                                 action=disable_module,
                                 classes='btn btn-info',
                                 visible=lambda m: m.installed and
                                 m.enabled)),
        )
    )

    def objects(self):
        return droplet.modules()

    def get_object(self, name):
        for module in droplet.modules():
            if module.name == name:
                return module

        raise KeyError('Module %s not found' % name)
