from django.db import models
from django.utils.translation import ugettext as _

from django.db.models.query import QuerySet


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



class ModelManager(models.Manager):
    """
    Model manager, it completely hides deleted objects, only exposed trough
    deleted method

    WARNING
    when subclassing this, if a custom manager is added, it should subclass
    this
    """

    def get_query_set(self):
        return ModelQuerySet(self.model).filter(_deleted=False)

    # Selectors

    def new(self):
        """
        Return the objects that were created since last module save
        """
        return self.get_query_set().filter(_new=True)

    def changed(self):
        """
        Return the objects that were modified since last module save
        """
        return self.get_query_set().filter(_changed=True)

    def deleted(self):
        """
        Return the objects that were deleted since last module save
        """
        return ModelQuerySet(self.model).filter(_deleted=True)


class Model(models.Model):
    """
    NAZS model, it stores configuration handled by modules

    WARNING
    when subclassing this, if a Meta class is added, it should
    subclass this (Model.Meta)
    """

    class Meta:
        abstract = True

    objects = ModelManager()

    # True if the object was added after module save event
    _new = models.BooleanField(default=True, verbose_name=_('Row new'))

    # True if the object has changed since last module save event
    _changed = models.BooleanField(default=True, verbose_name=_('Row changed'))

    # Deleted marker, custom manager will not show models with this set to True
    _deleted = models.BooleanField(default=False, verbose_name=_('Row deleted'))

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
    def commit_save(cls):
        """
        Process the module save event, this will:
            - Unmark updated objects
            - Unmark new objects
            - Completely delete objects mark as deleted
        """
        cls.objects.deleted().true_delete()
        cls.objects.changed().true_update(_new=False, _changed=False)


class ModuleInfo(Model):
    """
    NAZS module info, identified by the module name

    This models hold basic module info:
       - Module status

    """
    INSTALLED = 0
    DISABLED = 1
    ENABLED = 2

    STATUS_CHOICES = (
        (INSTALLED, _('Installed')),
        (DISABLED, _('Disabled')),
        (ENABLED, _('Enabled')),
       #(BROKEN, _('Broken')),
    )

    # Module name
    name = models.CharField(max_length=200, unique=True)

    # Status
    status = models.IntegerField(choices=STATUS_CHOICES, default=INSTALLED)

    # Changed
    changed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Module %s' % self.name

    class Meta(Model.Meta):
        verbose_name = _('Module')

