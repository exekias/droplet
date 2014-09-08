# -*- coding: utf-8 -*-
#
#  NAZS
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

from abc import ABCMeta
from collections import defaultdict
from django.conf import settings


class LocalCatalog(object):
    """
    Local catalog for registered class:`NAZSInterface` implementations, any
    interface implementation should be registered here in order to be
    accessible from catalog clients
    """

    #: Registered instances for class:`NAZSInterface` implementations
    INSTANCES = defaultdict(set)

    def register(self, cls, instance):
        """
        Register the given instance as implementation for a class interface
        """
        if not issubclass(cls, NAZSInterface):
            raise ValueError('Given class is not a NAZInterface subclass: %s'
                             % cls)

        if not isinstance(instance, cls):
            raise ValueError('Given instance does not implement the class: %s'
                             % instance)

        self.INSTANCES[cls].add(instance)

    def unregister(self, cls, instance):
        self.INSTANCES[cls].remove(instance)

    def get_instances(self, cls):
        return self.INSTANCES[cls]


# Global catalog
CATALOG = getattr(settings, 'NAZS_CATALOG', LocalCatalog())


class NAZSInterface(object):
    """
    NAZS service interface, base class for
    """

    __metaclass__ = ABCMeta

    def register(self):
        for cls in self.__class__.__bases__:
            if issubclass(cls, NAZSInterface):
                CATALOG.register(cls, self)

    def unregister(self):
        for cls in self.__class__.__bases__:
            if issubclass(cls, NAZSInterface):
                CATALOG.unregister(cls, self)
