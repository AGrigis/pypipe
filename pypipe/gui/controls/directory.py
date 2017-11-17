##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import Directory

# Third party import
from PySide import QtGui, QtCore
from ..timered_widgets import TimeredQLineEdit


class QtDirectory(QtGui.QWidget, Directory):
    """ Define a directory user selection control.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'QtDirectory' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        """
        super(QtDirectory, self).__init__()
        self._layout = QtGui.QHBoxLayout()
        self._default_value = value or ""
        self._init_ui() 
        Directory.__init__(self, value, *args, **kwargs)
        self.setLayout(self._layout)
        self._onedit()

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
        self._path = TimeredQLineEdit(self)
        self._path.setText(self._default_value)
        self._path.userModification.connect(self._onedit)
        self._layout.addWidget(self._path)
        self._button = QtGui.QPushButton('...', self)
        self._layout.addWidget(self._button)
        self._button.clicked.connect(self._onbrowse)

    def _onedit(self):
        """ Define the edit associated action.
        """
        self._set_value(self._path.text())

    def _onbrowse(self):
        """ Define the browse associated action.
        """
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, "Select directory", self._value or self._default_value)
        self._path.setText(directory)
        self._set_value(directory)

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
        is_valid = Directory._is_valid(self, value)
        p = self._path.palette()
        if is_valid:
            p.setColor(self._path.backgroundRole(), QtCore.Qt.white)
        else : 
            p.setColor(self._path.backgroundRole(), QtCore.Qt.red)
        self._path.setPalette(p)
        return is_valid
