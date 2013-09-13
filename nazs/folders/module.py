from nazs.core.module import Module

from models import Folder

import logging


logger = logging.getLogger(__name__)


class Folders(Module):
    """
    Abstract folder module, it holds information about folders
    managed by other modules

    This module will ensure that folders are created and with the correct
    permissions
    """

    def save(self):
        """
        Ensures all folders are created and with correct permissions
        """
        for folder in Folder.objects.all():
            folder.write()
