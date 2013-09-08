from nazs.core.sudo import set_euid
from nazs.core.module import Module
from django.db import settings


def init():
    """
    Initialize nazs environment, setup logging, processes and all
    needed stuff for running nazs
    """
    set_euid()


def save():

    for module in Module.MODULES:
        module = module()
        if module.installed:
            module.save()
