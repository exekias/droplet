__version__ = '0.1'
from django.db import settings

import importlib
import logging


def modules():
    """
    Return a list of instances of all present modules
    """
    from nazs.core.module import Module
    return [cls() for cls in Module.MODULES]


def changed():
    """
    Return True if there is any change in any of the available modules
    """
    for module in modules():
        if module.changed:
            return True
    return False


def save(**kwargs):
    """
    Apply configuration changes on all the modules
    """
    logger = logging.getLogger(__name__)
    logger.info("Saving changes")
    return

    # Save + restart
    for module in modules():
        if module.enabled:
            logger.info("Saving module: %s" % module.name)
            module.save()
            module.restart()
        else:
            logger.info("Not saving disabled module: %s" % module.name)

    # Commit
    for module in modules():
        module.commit()

    logger.info("Changes saved")


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    from nazs.core.sudo import set_euid
    set_euid()

    # Load all modules
    for app in settings.INSTALLED_APPS:
        try:
            importlib.import_module(app + '.module')
        except:
            pass
