##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os

# Package import
from .base import Base


class File(Base):
    """ Define a file parameter.
    """
    def _is_valid(self, value):
        """ A method used to check if the value is a file name.

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
        if isinstance(value, str) and os.path.isfile(value):
            return True
        else:
            return False
