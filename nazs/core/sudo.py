from django.conf import settings
from contextlib import contextmanager

import os
import pwd


def set_euid():
    """
    Set settings.RUN_AS_USER effective UID for the current process

    This adds some security, but nothing magic, an attacker can still
    gain root access, but at least we only elevate privileges when needed

    See root context manager
    """
    uid = int(pwd.getpwnam(settings.RUN_AS_USER).pw_uid)
    os.seteuid(uid)


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
    os.seteuid(0)
    yield
    set_euid()
