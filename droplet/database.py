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


class VolatileRouter(object):
    """
    Router to use special db for volatile models
    """
    def db_for_read(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile'
        return None

    def db_for_write(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, model):
        if db == 'volatile':
            return False
        return None

    def _model_volatile(self, model):
        if hasattr(model, 'volatile'):
            return model.volatile
        return False
