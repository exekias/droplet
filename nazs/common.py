from .util import import_module

import logging


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    from django.core import management
    # Sync volatile db, TODO set correct permissions
    management.call_command('syncdb', database='volatile', interactive=False)

    from .sudo import set_euid
    set_euid()

    # Load all modules
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        import_module(app + '.module')


def modules():
    """
    Return a list of instances of all present modules
    """
    from .module import Module
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
    from .models import ModuleInfo

    logger = logging.getLogger(__name__)
    logger.info("Saving changes")

    # Save + restart
    for module in modules():
        if module.enabled:
            if module.changed:
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
