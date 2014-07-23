from achilles.tables import *  # noqa


# OBJECT EDIT COLUMN

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


# TABLE ACTIONS

class TableAction(object):
    """
    Table action, executes an action on the whole table
    """
    creation_counter = 0

    def __init__(self, action, verbose_name=None, visible=lambda x: True,
                 classes='btn btn-default'):
        """
        :param verbose_name: Column human-readable name
        :param accessor: Function to access get data from the object
        :param visible: Function giving visibility flag for the given row
        :param action: Action to call
        :param classes: CSS classes to apply to the button
        """
        TableAction.creation_counter += 1
        self.creation_counter = TableAction.creation_counter
        self.verbose_name = verbose_name
        self.visible = visible
        self.action = action
        self.classes = classes

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

    def get_href(self):
        return ("javascript:achilles.action('web:table_action',"
                "['%s', '%s'])") % (self.table.register_name, self.name)

    def content(self):
        return '<a href="%s" class="%s">%s</a>' % \
               (self.get_href(), self.classes, self.verbose_name)

    def call(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class AddAction(TableAction):
    """
    Table object add action, show the given form to create a new item
    in the table
    """
    def __init__(self, form_name, *args, **kwargs):
        super(AddAction, self).__init__(None, *args, **kwargs)
        self.form_name = form_name

    def get_href(self):
        return ("javascript:achilles.loadInto(achilles.block('%s')"
                ".find('.pretable'), '%s')") % \
               (self.table.register_name, self.form_name)


# TABLE CLASS OVERRIDES


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
