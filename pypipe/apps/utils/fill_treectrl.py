##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Soma import
from PySide2 import QtWidgets
from PySide2 import QtGui

# Global parameters
font = QtGui.QFont("", 9, QtGui.QFont.Bold)


def fill_treectrl(treectrl, menu, match=""):
    """ Fill a tree control with the different menu items.

    This procedure is able to filter the menu items.
    Loadable functions appear in bold in the tree control.
    Insert four elements (current name, function module path, function
    input parameters, function output parameters)
    When the function module path is not None we have reached a leaf
    that contains a function description.

    Parameters
    ----------
    treectrl: QTreeControl (mandatory)
        the tree control where we want to insert the menu
    menu: hierachic dict (mandatory)
        each key is a sub module of the module. Leafs contain a list with
        the url to the documentation.
    match: str (optional)
        the string used to filter the menu items
    """
    treectrl.headerItem().setText(0, "Functions")
    add_tree_nodes(treectrl, menu, match)


def add_tree_nodes(parent_item, menu, match, parent_module=""):
    """ Add the menu to tree control if match in current module name or
    child modules.

    The match is insensitive to the cast.

    Parameters
    ----------
    parent_item: QTreeWidgetItem (mandatory)
        a tree control item where we want to insert the menu
    menu: hierachic dict (mandatory)
        each key is a sub module of the module. Leafs contain a list with
        the url to the documentation.
    match: str (mandatory)
        the string used to filter the menu items
    parent_module: str (optional)
        the parent module string description ('module.sub_module')
    """
    # Go through the current module sub modules
    for module_name, child_modules in menu.items():

        # Filtering: check if we need to add this module in the tree
        if (match == "" or match in module_name.lower() or
            search_in_menu(child_modules, match)):

            # Add the module name to the tree control
            if isinstance(child_modules, dict):
                tree_item = QtWidgets.QTreeWidgetItem(
                    parent_item, [module_name, "None", "None", "None"])
                if parent_module:
                    current_module = parent_module + "." + module_name
                else:
                    current_module = module_name
                add_tree_nodes(tree_item, child_modules, match, current_module)
            else:
                tree_item = QtWidgets.QTreeWidgetItem(
                    parent_item, [
                        module_name, child_modules[0], str(child_modules[1]),
                        str(child_modules[2])])
                tree_item.setFont(0, font)


def search_in_menu(menu, match):
    """ Recursive search in tree.

    The search procedure is insensitive to the cast.

    Parameters
    ----------
    menu: hierachic dict (mandatory)
        each key is a sub module of the module. Leafs contain a list with
        the url to the documentation.
    match: str (mandatory)
        the string used to filter the menu items

    Returns
    -------
    is_included: bool
        True if we found match in the tree, False otherwise.
    """
    # Initialize the default value: match not found
    is_included = False

    # If we are on a leaf, check in the module list
    if isinstance(menu, list):
        return is_included

    # Go through the current module sub modules
    for module_name, child_modules in menu.items():

        # Stop criteria
        if isinstance(child_modules, list):
            return is_included or match in module_name.lower()

        # Recursive search
        is_included = (
            is_included or match in module_name.lower() or
            search_in_menu(child_modules, match))

        # Stop criteria
        if is_included:
            return is_included

    return is_included
