import subprocess

def run(cmd):
    """
    executes a command on shell mode and returns stdout
    raises subprocess.CalledProcessError if it fails
    """

    output = subprocess.check_output(cmd, shell=True)

    return output

