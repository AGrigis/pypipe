##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import List

# Third party import
from PySide import QtGui, QtCore


class QtList(QtGui.QWidget, List):
    """ Define a list user control.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'QtList' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        """
        super(QtList, self).__init__()
        self._layout = QtGui.QHBoxLayout()
        self._init_ui() 
        List.__init__(self, value, *args, **kwargs)
        self._default_value = unicode(self._value or "")
        self.setLayout(self._layout)

    def reset(self):
        """ Reset the control to his initiale value.
        """
        self._int.setText(self._default_value)
        self._set_value(int(self._default_value))

    def _init_ui(self):
        """ Define the user interface.
        """
        raise NotImplementedError
