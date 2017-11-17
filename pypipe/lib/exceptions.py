##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Medule that defines the package custom exceptions.
"""


class ArgumentValidationError(ValueError):
    """ Raised when the type of an argument to a function is not what it
    should be.
    """
    def __init__(self, arg_num, func_name, accepted_arg_type):
        self.error = "The {0} argument of {1}() is not of {2}".format(
            arg_num, func_name, accepted_arg_type)

    def __str__(self):
        return self.error


class InvalidArgumentNumberError(ValueError):
    """ Raised when the number of arguments supplied to a function is
    incorrect.
    """
    def __init__(self, func_name):
        self.error = "Invalid number of arguments for {0}()".format(func_name)
 
    def __str__(self):
        return self.error


class InvalidReturnType(ValueError):
    """ Raised when a function return argument type is not what it should be.
    """
    def __init__(self, arg_num, func_name, accepted_arg_type):
        self.error = ("The {0} returned argument of {1}() is not of "
                      "{2}").format(arg_num, func_name, accepted_arg_type)

    def __str__(self):
        return self.error


class InvalidReturnNumberError(ValueError):
    """ Raised when the number of returned arguments supplied to a function is
    incorrect.
    """
    def __init__(self, func_name):
        self.error = "Invalid number of returned arguments for {0}()".format(
            func_name)
 
    def __str__(self):
        return self.error
