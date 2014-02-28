import subprocess
import logging


logger = logging.getLogger(__name__)


def run(cmd, background=False):
    """
    Executes the given command

    If background flag is True the command will run in background
    and this method will return a :class:`Popen` object

    If background is False (default) the command will run in this thread
    and this method will return stdout. A subprocess.CalledProcessError
    will be raised if command fails
    """
    logger.debug('Running command: %s' % cmd)

    if background:
        return subprocess.Popen(cmd, shell=True, close_fds=True)

    else:
        output = subprocess.check_output(cmd, shell=True,
                                         stderr=subprocess.STDOUT)
        if output:
            logger.debug('OUTPUT:\n' + output)
        return output
