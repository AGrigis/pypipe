##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import warnings
import logging

# Package import
from pypipe.lib.base import Observable


# Create a logger
logger = logging.getLogger(__name__)


class Base(Observable):
    """ Define an observable typed parameter.

    In order to test the parameter type, a '_is_valid' has to be
    specified. This function returned a boolean and take one parameter.

    Extra parameters are stored as class parameters.

    A 'None' value is interpreted as an undefined parameter.

    Attributes
    ----------
    `output`: bool
        tells us if the parameter is an output.
    `optional`: list
        tells us if the parameter is optional.
    `name`: string
        a name for the control.
    `iterable`: bool
        tells us if the control is iterable.
    `inner`: bool
        tells us if the control is an inner control.
    `copy`: bool
        tells us if the control value is changed during the processing and thus
        must be copied if some smart-caching strategies are used.
    `nohash`: bool
        tells us if the control must appear in the finger print of the function.
    """
    def __init__(self, value=None, is_output=False, is_optional=False,
                 *args, **kwargs):
        """ Initialize the 'Base' class.

        Parameters
        ----------
        value: object (optional, default None)
            the parameter value.
        is_output: bool (optional, default False)
            is the control an output or an input.
        is_optional: bool (optional, default False)
            is the control optional or not.
        """
        # Define private parameter to store the parameter value
        self._value = None

        # Define class parameters
        self.valid = False
        self.is_output = is_output
        self.is_optional = is_optional
        self.type = None
        self.name = ""
        self.iterable = False
        self.inner = False
        self.copy = False
        self.nohash = False
        self.kwargs = kwargs

        # Store extra parameters
        for pkey, pvalue in kwargs.items():
            setattr(self, pkey, pvalue)

        # Define a 'value' signal
        Observable.__init__(self, ["value"])

        # Set the initialized parameter value
        self._set_value(value)

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
        raise NotImplementedError("A '_is_valid' method has to be defined "
                                  "in child classes.")

    def _update_value(self, signal):
        """ Define an observer method that will update the current control
        value.

        Parameters
        ----------
        signal: SignalObject (mandatory)
            a signal object with a 'value' attribute.
        """
        if hasattr(signal, "value"):
            self._set_value(signal.value)
        else:
            raise ValueError(
                "Updating parameter '{0}'. "
                "Parameter update error {1}: observer signal has no attribute "
                "'value'.".format(self.name, type(self)))

    def _set_value(self, value):
        """ A method used to update the parameter value.

        Notify observers only if the new value is valid.

        Parameters
        ----------
        value: object (mandatory)
            the value we want to set.
        """
        logger.debug("Update value::")
        logger.debug("{0}: {1}".format(self.name, value))
        if not self.inner:
            if self._is_valid(value):
                self._value = value
                self.valid = True
                self.notify_observers("value", value=value, **self.kwargs)
            else:
                if self.is_optional and self.value is None:
                    self.valid = True
                else:
                    self.valid = False
                if self._value is not None:
                    warnings.warn(
                        "Updating parameter '{0}'. Parameter update "
                        "error {1}: old value '{2}'({3}), new value "
                        "'{4}'({5}).".format(self.name, type(self), self._value,
                                             type(self._value), value,
                                             type(value)))
        logger.debug("update: {0}".format(self.valid))
        logger.debug("Update value done.")

    value = property(lambda x: x._value, _set_value)
