import subprocess
import logging


logger = logging.getLogger(__name__)


def run(cmd):
    """
    executes a command on shell mode and returns stdout
    raises subprocess.CalledProcessError if it fails
    """

    logger.debug('Running command: %s' % cmd)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    logger.debug(output)

    return output
