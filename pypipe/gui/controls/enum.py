##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import Enum

# Third party import
from PySide import QtGui, QtCore
from ..timered_widgets import TimeredQLineEdit


class QtEnum(QtGui.QWidget, Enum):
    """ Define an enum user selection control.
    """
    def __init__(self, choices, value=None, *args, **kwargs):
        """ Initialize the 'QtEnum' class.

        Parameters
        ----------
        choices: list of str
            the different choices.
        value: object (optional, default None)
            the parameter value.
        """
        super(QtEnum, self).__init__()
        self._default_value = value
        Enum.__init__(self, value, choices=choices, *args, **kwargs)
        self._layout = QtGui.QHBoxLayout()
        self._init_ui() 
        self.setLayout(self._layout)

    def reset(self):
        """ Reset the control to his initiale value .
        """
        if self._default_value not in self.choices:
            self._combo.insertItem(0, "----Undefined----")
            self._combo.setCurrentIndex(0)
        self._set_value(self._default_value)

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

        # Add combo box to the layout
        self._combo = QtGui.QComboBox(self)        
        for item in self.choices :
            self._combo.addItem(item)
        if self._default_value not in self.choices:
            self._combo.insertItem(0, "----Undefined----")
            self._combo.setCurrentIndex(0)  
        else :
            self._combo.setCurrentIndex(self.choices.index(self._default_value))  
        self._combo.activated[str].connect(self._onselected)
        self._layout.addWidget(self._combo)

    def _onselected(self, text):
        """ Define the combo box selection associated action.
        """
        if self._value not in self.choices:
             self._combo.removeItem(0)
        self._set_value(text)

