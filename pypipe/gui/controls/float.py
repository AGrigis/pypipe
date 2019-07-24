##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import re

# Package import
from pypipe.lib.controls import Float

# Third party import
from PySide2 import QtWidgets, QtCore


class QtFloat(QtWidgets.QWidget, Float):
    """ Define a float user control.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'QtFloat' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        """
        super(QtFloat, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._default_value = value
        self._init_ui()
        Float.__init__(self, value, *args, **kwargs)
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Update layout
        self._layout.setSpacing(0)
        self._layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self._layout.setContentsMargins(0, 0, 0, 0)

        # Add line edit + brows button to the layout
        self._float = QtWidgets.QLineEdit(self)
        self._float.setText(
            str(self._default_value)
            if self._default_value is not None else "")
        self._float.textChanged.connect(self._onedit)
        self._layout.addWidget(self._float)

    def _onedit(self):
        """ Define the edit associated action.
        """
        evalue = self._float.text()
        evalue = evalue.replace(".", "", 1)
        evalue = re.sub("^([-+])", "", evalue, count=1)
        if evalue.isdigit():
            self._set_value(float(self._float.text()))
        else:
            self._set_value(self._float.text())

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
        is_valid = Float._is_valid(self, value)
        p = self._float.palette()
        if is_valid:
            p.setColor(self._float.backgroundRole(), QtCore.Qt.white)
        else : 
            p.setColor(self._float.backgroundRole(), QtCore.Qt.red)
        self._float.setPalette(p)
        return is_valid
