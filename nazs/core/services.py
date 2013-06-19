
class Service(object):
    """
    A service represents something that may be run

    This class is in charge of actions in order to get services to work
    and retrieve their status
    """

    # Available service states
    DISABLED = 0
    STOPPED = 1
    RUNNING = 2
    UNKNOWN = 3

    def status(self):
        return Service.UNKNOWN

    def is_running(self):
        return self.status() == Service.RUNNING


