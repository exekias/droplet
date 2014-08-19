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

import six
import importlib
import sys
import traceback


def import_module(module_path):
    """
    Try to import and return the given module, if it exists, None if it doesn't
    exist

    :raises ImportError: When imported module contains errors
    """
    if six.PY2:
        try:
            return importlib.import_module(module_path)
        except ImportError:
            tb = sys.exc_info()[2]
            stack = traceback.extract_tb(tb, 3)
            if len(stack) > 2:
                raise
    else:
        from importlib import find_loader
        if find_loader(module_path):
            return importlib.import_module(module_path)
