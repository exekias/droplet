from django.db import settings

from .models import ModuleInfo

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


def save():
    """
    Apply configuration changes on all the modules
    """
    logger = logging.getLogger(__name__)
    logger.info("Saving changes")

    # Save + restart
    for module in modules():
        if module.enabled:
            if module.changed:
                logger.info("Saving module: %s" % module.name)
                module.save()
                module.restart()
                module.commit()
            else:
                logger.debug("Not saving unchanged module: %s" % module.name)
        else:
            logger.debug("Not saving disabled module: %s" % module.name)

    # Commit
    ModuleInfo.commit()

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
