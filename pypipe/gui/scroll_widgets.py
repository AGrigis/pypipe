##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines a scroll widget.
"""

# Third party import
from PySide import QtCore, QtGui


class ScrollWidget(QtGui.QScrollArea):
    """ Class that create a scroll widget.

    The widget is placed in a scroll area when large sets of parameters have
    to be tuned.
    """
    def __init__(self, widget, parent=None, name=None):
        """ Method to initilaize the ScrollWidget class.

        Parameters
        ----------
        widget: QtGui.QWidget
            the widget that will be displayed in the scroll area.
        parent: QtGui.QWidget (optional, default None)
            the controller widget parent widget.
        name: (optional, default None)
            the name of this controller widget
        """
        # Inheritance
        super(ScrollWidget, self).__init__(parent)

        # Allow the application to resize the scroll area items
        self.setWidgetResizable(True)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
                           QtGui.QSizePolicy.Preferred)

        # Display a surounding box
        self.setFrameShape(QtGui.QFrame.StyledPanel)

        # Set the widget in the scroll area
        self.setWidget(widget)

