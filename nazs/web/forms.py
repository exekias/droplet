from achilles.forms import *  # noqa
from nazs.models import SingletonModel


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
