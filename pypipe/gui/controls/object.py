##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.lib.controls import Object

# Third party import
from PySide import QtGui, QtCore


class QtObjects(QtGui.QWidget, Object):
    """ Define a custom objects user control.
    """
    nb_item_per_line = 4

    def __init__(self, objects, value=None, otype=None, *args, **kwargs):
        """ Initialize the 'QtObjects' class.

        This control allows the user to choose an item from a list of objects.

        Parameters
        ----------
        objects: list
            a list of objects.
        value: object (optional, default None)
            the parameter value.
        otype: str (optional, default None)
            enable only objects of a certain type.
        """
        self._objects = objects
        self._default_value = value
        self._current_object = None
        self._valid_type = otype
        Object.__init__(self, value, *args, **kwargs)
        super(QtObjects, self).__init__()
        self._layout = QtGui.QGridLayout()
        self._init_ui()
        self.setLayout(self._layout)

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

        # Add grid check boxes to the layout
        n = len(self._objects)
        nb_rest_object = n % self.nb_item_per_line
        nb_full_lines = n // self.nb_item_per_line

        # > add full lines
        cnt = 0
        for i in range(nb_full_lines):
            for j in range(self.nb_item_per_line):
                button = QtGui.QRadioButton()
                otype = type(self._objects[cnt]).__name__
                button.setToolTip("This is a <b>{0}</b> object.".format(otype))
                button.setText(str(cnt))
                if self._default_value == cnt:
                    button.setChecked(True) 
                button.clicked.connect(self._onselected)
                if self._valid_type is not None:
                    button.setEnabled(self._valid_type == otype)
                self._layout.addWidget(button, i, j)
                cnt += 1

        # > add incomplete line
        for i in range(nb_rest_object):
            button = QtGui.QRadioButton()
            otype = type(self._objects[cnt]).__name__
            button.setToolTip("This is a <b>{0}</b> object.".format(otype))
            button.setText(str(cnt))
            if self._default_value == cnt:
                button.setChecked(True) 
            button.clicked.connect(self._onselected)
            if self._valid_type is not None:
                button.setEnabled(self._valid_type == otype)
            self._layout.addWidget(button, nb_full_lines, i)
            cnt += 1

        # > add create object check box
        if self.is_output:
            checkBox = QtGui.QRadioButton()
            checkBox.setText("New")
            if self._default_value == "New":
                checkBox.setChecked(True)
            checkBox.clicked.connect(self._onselected)
            self._layout.addWidget(checkBox, nb_full_lines + 1, 0)

    def _onselected(self):
        """ Define the selection associated action.
        """
        sender = self.sender()
        if sender.isChecked() :
            if self.is_output :
                self._current_object = sender.text()
            else:
                self._current_object = int(sender.text())
            self._set_value(self._objects[self._current_object])
        else:
            self._current_object = None
            self._set_value(None)
