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

from django.db.models import *  # noqa
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _


class ModelQuerySet(QuerySet):
    """
    Custom queryset

    to override update and delete actions
    """

    def update(self, **kwargs):
        """
        Update selected objects with the given keyword parameters
        and mark them as changed
        """
        super(ModelQuerySet, self).update(_changed=True, **kwargs)

    def delete(self):
        """
        Mark selected objects as deleted without deleting them
        """
        self.update(_deleted=True)

    # Only intended for internal use:

    def true_delete(self):
        """
        Totally delete the object from the table
        """
        super(ModelQuerySet, self).delete()

    def true_update(self, **kwargs):
        """
        Update the the object without marking it as changed
        """
        super(ModelQuerySet, self).update(**kwargs)


class ModelManager(Manager):
    """
    Model manager, it completely hides deleted objects, only exposed trough
    deleted method

    WARNING
    when subclassing this, if a custom manager is added, it should subclass
    this
    """
    def __init__(self, *args, **kwargs):
        super(ModelManager, self).__init__(*args, **kwargs)

        # updating model objects?
        self._updating = False

    def get_queryset(self):
        # Update model objects on each query
        if not self._updating:
            self._updating = True
            self.model.update()
            self._updating = False

        return ModelQuerySet(self.model).filter(_deleted=False)

    # Selectors

    def new(self):
        """
        Return the objects that were created since last module save
        """
        return self.get_queryset().filter(_new=True)

    def changed(self):
        """
        Return the objects that were modified since last module save
        """
        return self.get_queryset().filter(_changed=True)

    def deleted(self):
        """
        Return the objects that were deleted since last module save
        """
        return ModelQuerySet(self.model).filter(_deleted=True)


class Model(Model):
    """
    droplet model, it stores configuration handled by modules

    WARNING
    when subclassing this, if a Meta class is added, it should
    subclass this Model.Meta
    """

    class Meta:
        abstract = True

    objects = ModelManager()

    # True if the object was added after module save event
    _new = BooleanField(default=True,
                        verbose_name=_('Row new'),
                        editable=False)

    # True if the object has changed since last module save event
    _changed = BooleanField(default=True,
                            verbose_name=_('Row changed'),
                            editable=False)

    # Deleted marker, custom manager will not show models with this set to True
    _deleted = BooleanField(default=False,
                            verbose_name=_('Row deleted'),
                            editable=False)

    # Override save method to mark object as changed
    def save(self, *args, **kwargs):
        self._changed = True
        super(Model, self).save(*args, **kwargs)

    # Override delete method to mark object as changed
    def delete(self, *args, **kwargs):
        self._changed = True
        self._deleted = True
        super(Model, self).save(*args, **kwargs)

    @classmethod
    def update(cls):
        """
        Update model objects, used to map some external behavior
        from the system. This method will be called everytime the
        objects are accessed. This way you can update  objects after
        system changes (for example network interfaces)
        """
        pass

    @classmethod
    def commit(cls):
        """
        Commit current configuration, this will:
            - Unmark updated objects
            - Unmark new objects
            - Completely delete objects mark as deleted
        """
        cls.objects.deleted().true_delete()
        cls.objects.changed().true_update(_new=False, _changed=False)


class SingletonModel(Model):
    """
    One row Model, useful to store settings, to use it just instance like::

        settings = YourModel.get()
        settings.foo = True
        settings.save()
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class ModuleInfo(Model):
    """
    droplet module info, identified by the module name

    This models hold basic module info:
       - Module status

    """
    NOT_INSTALLED = 0
    DISABLED = 1
    ENABLED = 2

    STATUS_CHOICES = (
        (NOT_INSTALLED, _('Not installed')),
        (DISABLED, _('Disabled')),
        (ENABLED, _('Enabled')),
    )

    # Module name
    name = CharField(max_length=200, unique=True)

    # Status
    status = IntegerField(choices=STATUS_CHOICES, default=NOT_INSTALLED)

    # Changed
    changed = BooleanField(default=False)

    def __unicode__(self):
        return u'Module %s' % self.name

    class Meta(Model.Meta):
        verbose_name = _('Module')
