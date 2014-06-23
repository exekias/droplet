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
