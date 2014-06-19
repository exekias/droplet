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

        return (status, output)
