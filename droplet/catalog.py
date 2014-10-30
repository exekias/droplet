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

from abc import ABCMeta
from collections import defaultdict
from django.conf import settings


class LocalCatalog(object):
    """
    Local catalog for registered class:`DropletInterface` implementations, any
    interface implementation should be registered here in order to be
    accessible from catalog clients
    """
    # Registered instances for class:`DropletInterface` implementations
    INSTANCES_BY_INTERFACE = defaultdict(set)
    INSTANCES_BY_NAME = {}

    def register(self, cls, instance):
        """
        Register the given instance as implementation for a class interface
        """
        if not issubclass(cls, DropletInterface):
            raise TypeError('Given class is not a NAZInterface subclass: %s'
                            % cls)

        if not isinstance(instance, cls):
            raise TypeError('Given instance does not implement the class: %s'
                            % instance)

        if instance.name in self.INSTANCES_BY_NAME:
            if self.INSTANCES_BY_NAME[instance.name] != instance:
                raise ValueError('Given name is registered '
                                 'by other instance: %s' % instance.name)

        self.INSTANCES_BY_INTERFACE[cls].add(instance)
        self.INSTANCES_BY_NAME[instance.name] = instance

    def unregister(self, cls, instance):
        self.INSTANCES_BY_INTERFACE[cls].remove(instance)
        if instance.name in self.INSTANCES_BY_NAME:
            del self.INSTANCES_BY_NAME[instance.name]

    def get_instances(self, cls):
        return list(self.INSTANCES_BY_INTERFACE[cls])

    def get_instance_by_name(self, name):
        return self.INSTANCES_BY_NAME[name]


# Global catalog
_CATALOG = getattr(settings, 'DROPLET_CATALOG', LocalCatalog())


def get_instances(cls):
    if not issubclass(cls, DropletInterface):
        raise TypeError('%s should be a DropletInterface sublcass' % cls)

    return _CATALOG.get_instances(cls)


def get_instances_by_name(name):
    return _CATALOG.get_instance_by_name(name)


class DropletInterface(object):
    """
    droplet service interface, base class for
    """

    __metaclass__ = ABCMeta

    @property
    def name(self):
        """
        Return an unique name for the instance, this name should be the same
        between executions, and represents this object

        Default implementation is useful for singleton classes because it
        returns full python path to the class. Interfaces with multiple
        instances should override this to return an unique id
        """
        return '.'.join([self.__module__, self.__class__.__name__])

    def register(self):
        for cls in self.__class__.__bases__:
            if issubclass(cls, DropletInterface):
                _CATALOG.register(cls, self)

    def unregister(self):
        for cls in self.__class__.__bases__:
            if issubclass(cls, DropletInterface):
                _CATALOG.unregister(cls, self)
