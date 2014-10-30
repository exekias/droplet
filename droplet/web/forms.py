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

from achilles.forms import *  # noqa
from droplet.models import SingletonModel


# Override forms template
Form.template_name = 'web/form.html'


class ModelForm(ModelForm):

    def get_form(self, form_data=None, *args, **kwargs):
        # manage SingletonModels
        if issubclass(self.form_class.Meta.model, SingletonModel):
            instance = self.form_class.Meta.model.get()
            return self.form_class(form_data, instance=instance)
        else:
            return super(ModelForm, self).get_form(form_data, *args, **kwargs)
