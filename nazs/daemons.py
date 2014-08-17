from .sudo import root
from .commands import run

import logging

logger = logging.getLogger(__name__)


class Daemon(object):
    """
    Service represents a daemon that may be run. This class takes control on
    the status of the daemon and gives info about it
    """
    @property
    def running(self):
        """
        Return True if the daemon is running
        """
        raise NotImplementedError('You should implement this method')

    def start(self):
        """
        Start the daemon
        """
        logger.info("Starting daemon: %s" % self.name)
        self._start()

    def stop(self):
        """
        Stop the daemon
        """
        logger.info("Stopping daemon: %s" % self.name)
        self._stop()

    def restart(self):
        """
        Restart the daemon
        """
        logger.info("Restarting daemon: %s" % self.name)
        self._restart()

    def _start(self):
        raise NotImplementedError('You should implement this method')

    def _stop(self):
        raise NotImplementedError('You should implement this method')

    def _restart(self):
        self._stop()
        self._start()


class InitDaemon(Daemon):
    """
    Init managed daemon
    """
    def __init__(self, name):
        self.name = name

    def do(self, action):
        with root():
            return run('/usr/bin/service %s %s' % (self.name, action))

    @property
    def running(self):
        (status, output) = self.do('status')
        return 'running' in output

    def _start(self):
        self.do('start')

    def _stop(self):
        self.do('stop')

    def _restart(self):
        self.do('restart')
