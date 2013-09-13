from nazs.core.module import Module
from nazs.core.sudo import root
from nazs.core.commands import run
from nazs.core.files import TemplateConfFile

from models import Settings

import logging


logger = logging.getLogger(__name__)


class Torrent(Module):
    """
    Torrent download module based on transmission
    """
    settings = TemplateConfFile(
        '/var/lib/transmission-daemon/info/settings.json',
        template='torrent/settings.json',
        template_params=lambda: {
            'settings': Settings.get_or_create(),
        })

    def start(self):
        with root():
            run('/etc/init.d/transmission-daemon start')

    def stop(self):
        with root():
            run('/etc/init.d/transmission-daemon stop')

    def restart(self):
        with root():
            run('/etc/init.d/transmission-daemon reload')
