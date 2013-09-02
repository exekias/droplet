from django.conf import settings
from contextlib import contextmanager

import os
import pwd
import logging

logger = logging.getLogger(__name__)


def set_euid():
    """
    Set settings.RUN_AS_USER effective UID for the current process

    This adds some security, but nothing magic, an attacker can still
    gain root access, but at least we only elevate privileges when needed

    See root context manager
    """
    uid = int(pwd.getpwnam(settings.RUN_AS_USER).pw_uid)
    logger.debug('Current EUID is %s' % os.getuid())
    if uid != os.geteuid():
        try:
            os.seteuid(uid)
            logger.info('Set EUID to %s' % settings.RUN_AS_USER)
        except:
            current_user = pwd.getpwuid(os.getuid()).pw_name
            logger.error("Failed to set '%s' EUID, running as '%s'" %
                         (settings.RUN_AS_USER, current_user))
            raise e
    else:
        logger.debug('Didn\'t set EUID, it was already correct')


def drop_privileges():
    """
    Set settings.RUN_AS_USER UID for the current process

    After calling this, root operation will be impossible to execute

    See root context manager
    """
    uid = int(pwd.getpwnam(settings.RUN_AS_USER).pw_uid)
    os.setuid(uid)


@contextmanager
def root():
    """
    Run the enclosed code as root (uid 0)

    Usage:

    with root():
        ...

    """
    logger.info('Entering ROOT mode')
    os.seteuid(0)
    yield
    os.seteuid(int(pwd.getpwnam(settings.RUN_AS_USER).pw_uid))
    logger.info('Exited ROOT mode')
