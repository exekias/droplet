from achilles.tables import ButtonColumn


class EditColumn(ButtonColumn):
    """
    Action to show a form for the given object
    """
    def __init__(self, form, classes='', *args, **kwargs):
        super(EditColumn, self).__init__(*args, **kwargs)
        self.form = form
        self.classes = classes

    def get_href(self, obj):
        return ("javascript:achilles.loadInto(achilles.block('%s')"
                ".find('.pretable'), '%s', ['%s',])") % (
                self.table.register_name, self.form, obj.id)
