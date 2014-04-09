#!/usr/bin/env python
import os
import sys

# Activate nazs env
manage_path = os.path.dirname(os.path.realpath(__file__))
activate_this = os.path.join(manage_path, '/usr/share/python/nazs/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

os.environ['DJANGO_SETTINGS_MODULE'] = 'nazs.settings'

import nazs
nazs.init()

from django.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
