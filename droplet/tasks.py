# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import django.dispatch


class Task(object):
    """
    Tasks are pieces of work to be done by modules
    """
    #: Signal dispatched before running this task
    prerun = django.dispatch.Signal()

    #: Signal dispatched after running this task
    postrun = django.dispatch.Signal()

    #   success ?
    #   failure ?

    def __init__(self, name):
        self.name = name

    def run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    @property
    def __name__(self):
        return self.name

    def __repr__(self):
        return 'Task \'%s\'' % self.name


class CallableTask(Task):
    """
    Task that uses a callable as run function
    """
    def __init__(self, func):
        name = getattr(func, '_decorated_function', func).__name__

        # Add class name for method callables
        if hasattr(func, 'im_class'):
            name = '.'.join(func.im_class.__name__, name)

        self.func = func
        super(CallableTask, self).__init__(name)

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def task(func=None):
    """
    Decorator for quick :class:`Task` creation, it takes a callable and
    returns a :class:`Task` object which will call it on run
    """
    if func is None:
        return task

    return CallableTask(func)
