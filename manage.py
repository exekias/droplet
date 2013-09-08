#!/usr/bin/env python
import os
import sys

# Include . in python path
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nazs.settings'

# Activate virtual env
manage_path = os.path.dirname(os.path.realpath(__file__))
activate_this = os.path.join(manage_path, 'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# If we import this here coverage info will be wrong
#from nazs.core.common import init
#init()

from django.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
