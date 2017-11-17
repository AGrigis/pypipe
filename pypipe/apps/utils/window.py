##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from pypipe.apps.resources.icones import *

# Third party import
from PySide.QtUiTools import QUiLoader


class MyQUiLoader(object):
    """ Base window class based on ui file description.
    """

    def __init__(self, uifile):
        """ Method to initialize the base window.

        Parameters
        ----------
        uifile: str (mandatory)
            a filename containing the user interface description.
        """
        self.ui = QUiLoader().load(uifile)
