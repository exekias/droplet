import nazs


class MenuItem(object):
    """
    Menu item
    """
    def __init__(self, name, url=None, verbose_name=None):
        self.name = name
        self.verbose_name = verbose_name or name
        self.url = url
        self.items = []

    def append(self, item):
        """
        Add the given item as children
        """
        if self.url:
            raise TypeError('Menu items with URL cannot have childrens')

        # Look for already present common node
        if not item.is_leaf():
            for current_item in self.items:
                if item.name == current_item.name:
                    for children in item.items:
                        current_item.append(children)
                    return

        # First insertion
        self.items.append(item)

    def is_leaf(self):
        return not self.items


def menu():
    """
    Return global menu composed from all modules menu.

    This method will compose the global menu by calling menu() function for
    module, it should be located under module_path.web.menu module
    """
    root = MenuItem('')

    for mod in nazs.modules():
        if mod.installed:
            module_path = mod.__class__.__module__.rsplit('.', 1)[0]
            menu = nazs.util.import_module(module_path + '.web.menu')
            if menu:
                menu.menu(root)

    return root
