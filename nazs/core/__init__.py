from nazs.core.sudo import set_euid


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    set_euid()
