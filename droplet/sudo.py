# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from contextlib import contextmanager

import os
import pwd
import logging

logger = logging.getLogger(__name__)


def set_euid():
    """
    Set settings.DROPLET_USER effective UID for the current process

    This adds some security, but nothing magic, an attacker can still
    gain root access, but at least we only elevate privileges when needed

    See root context manager
    """
    current = os.geteuid()
    logger.debug("Current EUID is %s" % current)

    if settings.DROPLET_USER is None:
        logger.info("Not changing EUID, DROPLET_USER is None")
        return

    uid = int(pwd.getpwnam(settings.DROPLET_USER).pw_uid)
    if current != uid:
        try:
            os.seteuid(uid)
            logger.info("Set EUID to %s (%s)" %
                        (settings.DROPLET_USER, os.geteuid()))
        except:
            current_user = pwd.getpwuid(os.getuid()).pw_name
            logger.error("Failed to set '%s' EUID, running as '%s'" %
                         (settings.DROPLET_USER, current_user))
    else:
        logger.debug("Didn't set EUID, it was already correct")


def drop_privileges():
    """
    Set settings.DROPLET_USER UID for the current process

    After calling this, root operation will be impossible to execute

    See root context manager
    """
    uid = int(pwd.getpwnam(settings.DROPLET_USER).pw_uid)
    os.setuid(uid)


@contextmanager
def root():
    """
    Run the enclosed code as root (uid 0)

    Usage:

    with root():
        ...

    """
    logger.debug('Entering ROOT mode')
    old_euid = os.geteuid()
    os.seteuid(0)
    yield
    os.seteuid(old_euid)
    logger.debug('Exited ROOT mode')
