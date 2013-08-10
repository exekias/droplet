from nazs.core.sudo import drop_privileges

def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    drop_privileges()

