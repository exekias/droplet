# -*- coding: utf-8 -*-
#
#  NAZS
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

from .util import import_module

import logging
import os


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    from django.core import management
    from django.conf import settings

    from .sudo import set_euid
    set_euid()

    # Sync volatile db and set permissions
    volatile_db = settings.DATABASES['volatile']['NAME']
    management.call_command('syncdb',
                            database='volatile',
                            interactive=False,
                            verbosity=0)
    os.chmod(volatile_db, 0600)

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
