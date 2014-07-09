from achilles.forms import *  # noqa
from nazs.models import SingletonModel


# Override forms template
FormBlock.template_name = 'web/form.html'

# Show a save button by default
FormBlock.save_button = True


class ModelFormBlock(ModelFormBlock):

    def get_form(self, form_data=None, *args, **kwargs):
        # manage SingletonModels
        if issubclass(self.form_class.Meta.model, SingletonModel):
            instance = self.form_class.Meta.model.get()
            return self.form_class(form_data, instance=instance)
        else:
            return super(ModelFormBlock, self).get_form(*args, **kwargs)
