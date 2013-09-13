from django.db import models
from django.utils.translation import ugettext as _

from nazs.core.models import Model
from nazs.core.sudo import root

import logging
import pwd
import grp
import os


logger = logging.getLogger(__name__)


class Folder(Model):
    """
    A folder in the system
    """
    def __init__(self, *args, **kwargs):
        super(Folder, self).__init__(*args, **kwargs)

        # Dirty hack to set uid/gid choices in runtime
        self._meta.get_field_by_name('uid')[0]._choices = self._uid_choices()
        self._meta.get_field_by_name('gid')[0]._choices = self._gid_choices()

    # Visible name
    name = models.CharField(max_length=10)

    # Full path of the folder
    path = models.CharField(max_length=250)

    # Folder permissions (octal)
    mode = models.IntegerField(default=0755)

    # Owner
    uid = models.IntegerField(default=0)

    # Group
    gid = models.IntegerField(default=0)

    def write(self):
        """
        Create the folder with the correct permissions and ownership
        """
        with root():
            if not os.path.exists(self.path):
                logger.info("Creating %s" % self.path)
                os.makedirs(self.path, self.mode)
            else:
                logger.debug("%s already exists" % self.path)

            # set permissions
            os.chmod(self.path, self.mode)
            os.chown(self.path, self.uid, self.gid)

    def _uid_choices(self):
        for user in pwd.getpwall():
            yield (user.pw_uid, user.pw_name)

    def _gid_choices(self):
        for group in grp.getgrall():
            yield (group.gr_gid, group.gr_name)

    def __unicode__(self):
        return self.name
