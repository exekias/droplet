from django.db import settings
from django.db.models.signals import post_save

from nazs.core.sudo import set_euid
from nazs.core.module import Module

import importlib
import logging


logger = logging.getLogger(__name__)


def conf_change(**kwargs):
    """
    Apply configuration change son all the modules
    """
    logger.info("Saving changes")

    for cls in Module.MODULES:
        module = cls()
        if module.enabled:
            logger.info("Saving module: %s" % module.name)
            module.save()
            module.restart()
        else:
            logger.info("Not saving disabled module: %s" % module.name)

    logger.info("Changes saved")


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    set_euid()

    # Load all modules
    for app in settings.INSTALLED_APPS:
        try:
            importlib.import_module(app + '.module')
        except:
            pass

    # DEVELOPMENT ONLY: save on model change
    post_save.connect(conf_change)
