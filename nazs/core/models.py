from django.db import models
from django.utils.translation import ugettext as _


class ModuleInfo(models.Model):
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
    name = models.CharField(max_length=200)

    # Status
    status = models.IntegerField(choices=STATUS_CHOICES, default=INSTALLED)

    # Changed
    changed = models.BooleanField(default=False)

