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

from django.core.urlresolvers import reverse

from droplet.web import redirect
from droplet.actions import Library
from droplet import save


register = Library('core')


@register.action
def install_module(transport, table, module):
    # Go to wizard if module declares one
    if module.install_wizard:
        wizard_url = reverse('wizard', kwargs={'block': module.install_wizard})
        redirect.redirect(transport, wizard_url)
        return

    module.install()
    module.enable()


@register.action
def enable_module(transport, table, module):
    module.enable()


@register.action
def disable_module(transport, table, module):
    module.disable()


@register.action
def apply_changes(transport):
    save()
