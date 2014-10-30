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

import droplet

from droplet.util import import_module


class MenuItem(object):
    """
    Menu item
    """
    def __init__(self, name, url=None, verbose_name=None):
        self.name = name
        self.verbose_name = verbose_name or name
        self.url = url
        self.items = []

    def append(self, item):
        """
        Add the given item as children
        """
        if self.url:
            raise TypeError('Menu items with URL cannot have childrens')

        # Look for already present common node
        if not item.is_leaf():
            for current_item in self.items:
                if item.name == current_item.name:
                    for children in item.items:
                        current_item.append(children)
                    return

        # First insertion
        self.items.append(item)

    def is_leaf(self):
        return not self.items


def menu():
    """
    Return global menu composed from all modules menu.

    This method will compose the global menu by calling menu() function for
    module, it should be located under module_path.menu module
    """
    root = MenuItem('')

    for mod in droplet.modules():
        if mod.installed:
            module_path = mod.__class__.__module__.rsplit('.', 1)[0]
            menu = import_module(module_path + '.menu')
            if menu:
                menu.menu(root)

    return root
