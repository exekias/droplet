from django.template.loader import get_template
from django.template import Context

from nazs.core.sudo import root

import os
import pwd
import grp


class ConfFile(object):
    """
    ConfFile is the representation of any configuration file that a module will
    write in order to work
    """
    def __init__(self, path, mode=None, user='root', group='root'):
        """
        Instance a ConfFile object

        Parameters
            path - full path of the file
            mode - POSIX permissions mode
            user - owner of the file
            group - group of the file
        """
        self.path = path
        self.mode = mode
        self.user = user
        self.group = group

    def write(self):
        """
        Write the file, forcing the proper permissions
        """
        mode = self.mode or 0640

        oldmask = os.umask(0)

        with root():
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT, mode)
            with os.fdopen(fd, 'w') as f:
                os.fchown(fd, self.uid(), self.gid())
                f.write(self.contents())

        os.umask(oldmask)

    def contents(self):
        """
        Return contents to write in the file
        """
        return ''

    def uid(self):
        return int(pwd.getpwnam(self.user).pw_uid)

    def gid(self):
        return int(grp.getgrnam(self.group).gr_gid)


class TemplateConfFile(ConfFile):

    def __init__(self, path, template=None,
                 template_params={}, *args, **kwargs):
        self.template = template
        self.template_params = template_params
        super(TemplateConfFile, self).__init__(path, *args, **kwargs)

    def contents(self):
        template = get_template(self.template)
        if callable(self.template_params):
            params = self.template_params()
        else:
            params = self.template_params
        context = Context(params)
        return template.render(context)
