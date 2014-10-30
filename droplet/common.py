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

import logging


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
                logger.debug('Not saving unchanged module: %s' %
                             module.verbose_name)
        else:
            logger.debug('Not saving disabled module: %s' %
                         module.verbose_name)

    # Commit
    ModuleInfo.commit()

    logger.info("Changes saved")
