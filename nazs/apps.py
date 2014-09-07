from django.apps import AppConfig

import os
import pkg_resources


class NAZSConfig(AppConfig):
    name = 'nazs'

    def ready(self):
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
        for app in pkg_resources.iter_entry_points('nazs.app'):
            __import__(app.module_name + '.module')
