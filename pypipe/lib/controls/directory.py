##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os

# Package import import
from .base import Base


class Directory(Base):
    """ Define a directory parameter.
    """
    def _is_valid(self, value):
        """ A method used to check if the value is a directory.

        Parameters
        ----------
        value: str (mandatory)
            a path to a directory.

        Returns
        -------
        is_valid: bool
            return True if the value is a directory,
            False otherwise.
        """
        if isinstance(value, str) and os.path.isdir(value):
            return True
        else:
            return False
