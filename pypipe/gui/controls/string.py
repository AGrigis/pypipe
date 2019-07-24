##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import String

# Third party import
from PySide2 import QtWidgets, QtCore
from ..timered_widgets import TimeredQLineEdit


class QtString(QtWidgets.QWidget, String):
    """ Define a string user control.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'QtString' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        """
        super(QtString, self).__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self._init_ui() 
        String.__init__(self, value, *args, **kwargs)
        self._default_value = self._value or ""
        self.setLayout(self._layout)
        self.reset()

    def reset(self):
        """ Reset the control to his initiale value.
        """
        self._text.setText(self._default_value)
        self._set_value(self._default_value)

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
        self._text = TimeredQLineEdit(self)
        self._text.textChanged.connect(self._onedit)
        self._layout.addWidget(self._text)

    def _onedit(self):
        """ Define the edit associated action.
        """
        self._set_value(self._text.text())

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
        is_valid = String._is_valid(self, value)
        p = self._text.palette()
        if is_valid:
            p.setColor(self._text.backgroundRole(), QtCore.Qt.white)
        else : 
            p.setColor(self._text.backgroundRole(), QtCore.Qt.red)
        self._text.setPalette(p)
        return is_valid
