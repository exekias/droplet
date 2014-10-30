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

from __future__ import absolute_import
import commands
import subprocess
import logging


logger = logging.getLogger(__name__)


class CommandException(Exception):
    def __init__(self, status, output):
        self.status = status
        self.output = output

    def __str__(self):
        return self.output


def run(cmd, background=False):
    """
    Executes the given command

    If background flag is True the command will run in background
    and this method will return a :class:`Popen` object

    If background is False (default) the command will run in this thread
    and this method will return stdout.

    A CommandException will be raised if command fails
    """
    logger.debug('Running command: %s' % cmd)

    if background:
        return subprocess.Popen(cmd, shell=True, close_fds=True)

    else:
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            logger.error("Command failed: %s" % cmd)

        if output:
            logger.debug('OUTPUT:\n' + output)

        if status != 0:
            raise CommandException(status, output)

        return output
