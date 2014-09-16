from django.utils.translation import ugettext as _
from nazs import models

import os


class ListenPort(models.Model):
    """
    Apache listen ports
    """
    port = models.PositiveIntegerField(primary_key=True)

    ssl = models.BooleanField(default=False)


class CommonConfFile(models.Model):
    """
    Common class for apache conf files (with availabe/enabled behavior)

    This class expects the following fields to be defined:

      AVAILABLE_PATH - full path for available items
      ENABLED_PATH - full path for enabled items
      EXTENSION - items file extension
    """
    name = models.CharField(primary_key=True, max_length=100, editable=False,
                            verbose_name=_('Name'))

    enabled = models.BooleanField(default=False, verbose_name=_('Enabled'))

    #: modified by the system (user didn't touch it)
    system = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.__class__.objects._updating:
            # user modified the item, no longer a system one
            self.system = False

        super(CommonConfFile, self).save(*args, **kwargs)

    @classmethod
    def update(cls):
        available = [mod[:-len(cls.EXTENSION)-1]
                     for mod in os.listdir(cls.AVAILABLE_PATH)
                     if mod.endswith(cls.EXTENSION)]

        enabled = [mod[:-len(cls.EXTENSION)-1]
                   for mod in os.listdir(cls.ENABLED_PATH)
                   if mod.endswith(cls.EXTENSION)]

        for item in available:
            item_enabled = item in enabled
            try:
                item = cls.objects.get(name=item)

                if item.enabled != item_enabled:
                    # bring system changes if user didn't touch it
                    if item.system:
                        item.enabled = item_enabled
                    # mark as changed in any way (user enforced ones need save)
                    item.save()

            except cls.DoesNotExist:
                cls(name=item, enabled=item_enabled, system=True).save()

        cls.objects.exclude(name__in=available).delete()


class Module(CommonConfFile):
    """
    Apache modules
    """
    AVAILABLE_PATH = '/etc/apache2/mods-available/'
    ENABLED_PATH = '/etc/apache2/mods-enabled/'
    EXTENSION = 'load'


class Conf(CommonConfFile):
    """
    Apache conf file
    """
    AVAILABLE_PATH = '/etc/apache2/conf-available/'
    ENABLED_PATH = '/etc/apache2/conf-enabled/'
    EXTENSION = 'conf'
