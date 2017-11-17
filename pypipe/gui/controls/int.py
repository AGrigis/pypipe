##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import Int

# Third party import
from PySide import QtGui, QtCore


class QtInt(QtGui.QWidget, Int):
    """ Define an integer user control.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'QtInt' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        """
        super(QtInt, self).__init__()
        self._layout = QtGui.QHBoxLayout()
        self._default_value = value
        self._init_ui() 
        Int.__init__(self, value, *args, **kwargs)
        self.setLayout(self._layout)
        self._onedit()

    def reset(self):
        """ Reset the control to his initiale value.
        """
        self._int.setText(self._default_value)
        self._set_value(int(self._default_value))

    def _init_ui(self):
        """ Define the user interface.
        """
        # Resize widget
        self.resize(1000, 27)

        # Define size policy
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Update layout
        self._layout.setSpacing(0)
        self._layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # Add line edit + brows button to the layout
        self._int = QtGui.QLineEdit(self)
        self._int.setText(
            str(self._default_value)
            if self._default_value is not None else "")
        self._int.textChanged.connect(self._onedit)
        self._layout.addWidget(self._int)

    def _onedit(self):
        """ Define the edit associated action.
        """
        evalue = self._int.text()
        if evalue.isdigit():
            self._set_value(int(evalue))
        else:
            self._set_value(evalue)

    def _is_valid(self, value):
        """ Overload the validation function.

        Parameters
        ----------
        value: str (mandatory)
            a file name.

        Returns
        -------
        is_valid: bool
            return True if the value is a file,
            False otherwise.
        """
        is_valid = Int._is_valid(self, value)
        p = self._int.palette()
        if is_valid:
            p.setColor(self._int.backgroundRole(), QtCore.Qt.white)
        else : 
            p.setColor(self._int.backgroundRole(), QtCore.Qt.red)
        self._int.setPalette(p)
        return is_valid
