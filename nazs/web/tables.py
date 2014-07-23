from achilles.tables import *  # noqa


# Edit Column

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
                ".find('.pretable'), '%s', ['%s',])") % \
               (self.table.register_name, self.form, obj.id)


# Global Table Actions

class TableAction(object):
    """
    Table action, executes an action on the whole table
    """
    creation_counter = 0

    def __init__(self, verbose_name=None,
                 visible=lambda x: True):
        """
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        :param visible: Function giving visibility flag for the given row
        """
        TableAction.creation_counter += 1
        self.creation_counter = TableAction.creation_counter
        self.verbose_name = verbose_name
        self.visible = visible

    def contribute_to_class(self, table, name):
        self.name = name
        self.verbose_name = self.verbose_name or name
        self.table = table

    def render(self):
        """
        Render table action button
        """
        if self.visible(self.table):
            return self.content()
        else:
            return ''

    def content(self):
        return self.verbose_name


class Table(Table):
    # Override table template
    Table.template_name = 'web/table.html'

    def actions(self):
        """
        List of :class:`TableAction` elements defined for this table
        """
        actions = []
        for a in dir(self):
            a = getattr(self, a)
            if isinstance(a, TableAction):
                actions.append(a)

        # We are not caching this because array len should be low enough
        actions.sort(key=lambda action: action.creation_counter)
        return actions
