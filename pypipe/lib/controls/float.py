##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from .base import Base


class Float(Base):
    """ Define a float parameter.
    """
    def _is_valid(self, value):
        """ A method used to check if the value is valid.

        Parameters
        ----------
        value: object (mandatory)
            a string.

        Returns
        -------
        is_valid: bool
            return True if the value is a float,
            False otherwise.
        """
        if isinstance(value, float):
            return True
        else:
            return False
