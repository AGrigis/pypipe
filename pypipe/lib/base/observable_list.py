##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


"""
Module that defines an observable list from the observable pattern design.
"""


# Package import
from .observable import Observable


class ObservableList(list, Observable):
    """ Create an observable list.

    This class acts as a python list object.

    The 'append', 'pop', 'insert' and 'remove' methods have been overloaded in
    order to notify some observers. The associated signals have the same names.
    """

    def __init__(self, sequence=[]):
        """ Initilaize the ObservableList class.

        Parameters
        ----------
        sequence: list
            the init list.
        """
        list.__init__(self, sequence)
        Observable.__init__(self, ["append", "pop", "insert", "remove"])

    def append(self, value):
        """ Overlaod the append method.

        Parameters
        ----------
        value: object
            the value that will be added in the list.
        """
        list.append(self, value)
        self.notify_observers("append", value=value)
    
    def pop(self, *args):
        """ Overlaod the pop method.
        """
        value = list.pop(self, *args)
        self.notify_observers("pop", value=value)
        return value

    def insert(self, index, value):
        """ Overload the insert method.

        Parameters
        ----------
        index: int
            where to insert the new element.
        value: object
            the value that will be inserted in the list.
        """
        list.insert(self, index, value)
        self.notify_observers("insert", value=value, index=index)

    def remove(self, value):
        """ Overload the remove method.

        Parameters
        ----------
        value: object
            the value that will be removed from the list.
        """
        list.remove(self, value)
        self.notify_observers("remove", value=value)
