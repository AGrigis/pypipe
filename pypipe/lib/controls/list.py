##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Package import
from .base import Base


class List(Base):
    """ Define a list parameter.
    """
    def __init__(self, value=None, *args, **kwargs):
        """ Initialize the 'List' class.

        Expect a 'content' string argument that describe the list content.

        Parameters
        ----------
        content: str (mandatory)
            description of the list content. If iterative object are contained
            use the '_' character as a separator: 'Int' or 'List_Int'.
        value: object (optional, default None)
            the parameter value.
        """
        # Avoid cycling import
        from pypipe.lib.controls import controls

        # Check if a 'content' argument has been defined
        if "content" not in kwargs:
            raise ValueError("A 'content' argument  describing the 'List' "
                             "content is expected.")

        # Create an inner control
        inner_desc = kwargs["content"].split("_")
        control_type = inner_desc[0]
        inner_kwargs = {"inner": True}
        if len(inner_desc) > 1:
            inner_kwargs["content"] = "_".join(inner_desc[1:])
        if control_type not in controls:
            raise ValueError("List creation: '{0}' is not a valid inner "
                             "control type. Allowed types are {1}.".format(
                                 kwargs["content"], controls.keys()))
        self.inner_control = controls[control_type](**inner_kwargs)

        # Create the list control
        Base.__init__(self, value, *args, **kwargs)
        self.iterable = True

    def _is_valid(self, value):
        """ A method used to check the value type.

        Parameters
        ----------
        value: object (mandatory)
            the value we want to check the type.

        Returns
        -------
        is_valid: bool
            return True if the value as the expected type,
            False otherwise.
        """
        if value is None:
            return True
        elif isinstance(value, list):
            for item in value:
                if not self.inner_control._is_valid(item):
                    return False
            return True
        else:
            return False
