##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import __builtin__
import re
import inspect
import logging
import importlib
import functools

# Package import
from .exceptions import ArgumentValidationError
from .exceptions import InvalidArgumentNumberError
from .exceptions import InvalidReturnType
from .exceptions import InvalidReturnNumberError


# Create a logger
logger = logging.getLogger(__name__)


# Global parameters
TYPES = [t for t in __builtin__.__dict__.itervalues() if isinstance(t, type)]


def ordinal(num):
    """ Compute the ordinal number of a given integer, as a string.

    Parameters
    ----------
    num: int
        an integer.

    Returns
    -------
    ordinal: str
        the ordinal representation of the input integer, eg. 1 -> 1st,
        2 -> 2nd, 3 -> 3rd, etc.
    """
    if 10 <= num % 100 < 20:
        return "{0}th".format(num)
    else:
        ord = {1 : "st", 2 : "nd", 3 : "rd"}.get(num % 10, "th")
        return "{0}{1}".format(num, ord)


def inputs(*accepted_arg_types):
    """ A decorator to validate the parameter types of a given function.

    It is passed a tuple, eg. (<type 'tuple'>, <type 'int'>, 'file'), and
    checks only types. This tuple is stored in the '_input_types' function
    attribute.
 
    Note: It doesn't do a deep check, for example checking through a
          tuple of types.
    """
    def input_decorator(validate_function):
        """ Decorate the 'validate_function' function.
        """
        # Store the accepted args in function parameter
        setattr(validate_function, "_input_types", accepted_arg_types)

        @functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            """ Define a sub-decorator to check the function parameters.
            """
            nb_args = len(function_args) + len(function_args_dict)
            if len(accepted_arg_types) != nb_args:
                raise InvalidArgumentNumberError(validate_function.__name__)
 
            for arg_num, (actual_arg, accepted_arg_type) in enumerate(
                    zip(function_args, accepted_arg_types)):
                if accepted_arg_type not in TYPES:
                    continue
                if type(actual_arg) is not accepted_arg_type:
                    ord_num = ordinal(arg_num + 1)
                    raise ArgumentValidationError(ord_num,
                                                  validate_function.__name__,
                                                  accepted_arg_type)
            return validate_function(*function_args, **function_args_dict)
        return decorator_wrapper
    return input_decorator


def returns(*accepted_return_type_tuple):
    """ Decorator to set the return types.

    It is passed a tuple, eg. (<type 'tuple'>, <type 'int'>, 'file'), and
    checks only types. This tuple is stored in the '_output_types' function
    attribute.
 
    Note: It doesn't do a deep check, for example checking through a
          tuple of types.
    """
    def return_decorator(validate_function):
        """ Decorate the 'validate_function' function.
        """
        # Store the returned args in function parameter
        setattr(validate_function, "_output_types", accepted_return_type_tuple)
 
    	@functools.wraps(validate_function)
        def decorator_wrapper(*function_args, **function_args_dict):
            """ Define a sub-decorator to check the function parameters.
            """
            return_values = validate_function(
                *function_args, **function_args_dict)
            if return_values is None and len(accepted_return_type_tuple) == 0:
                return return_values
            flatten = False
            if not isinstance(return_values, tuple):
                flatten = True
                return_values = (return_values, )

            if len(return_values) != len(accepted_return_type_tuple):
                raise InvalidReturnNumberError(validate_function.__name__)

            for arg_num, (return_value, accepted_return_type) in enumerate(
                    zip(return_values, accepted_return_type_tuple)):
                if accepted_return_type not in TYPES:
                    continue
                if type(return_value) is not accepted_return_type:
                    ord_num = ordinal(arg_num + 1)
                    raise InvalidReturnType(ord_num,
                                            validate_function.__name__,
                                            accepted_return_type)

            if flatten:
                return_values = return_values[0]
            return return_values
        return decorator_wrapper
    return return_decorator


def load_func_from_module_path(func_module_path, input_arg_types,
                               output_arg_types, input_meta=None,
                               output_meta=None):
    """ Load a function fom its module description.

    Parameters
    ----------
    func_module_path: str
        the function module description: <a>.<b>.<c>.py
    input_arg_types: tuple
        the function input arguments types.
    output_arg_types: tuple
        the function output arguments types.
    input_meta: tuple
        the function input parameters associated metadata.
    output_meta: tuple
        the function input parameters associated metadata.

    Returns
    -------
    func: callable
        the loaded function with special attributes: '_input_types',
        '_output_types', '_input_names', '_output_names',
        '_default_values', _'input_meta', and 'output_meta'.
    """
    # Check input parameters
    if input_meta is not None:
        assert len(input_arg_types) == len(input_meta)
    if output_meta is not None:
        assert len(output_arg_types) == len(output_meta)

    # Load the function
    logger.debug("Loading function '{0}'::".format(func_module_path))
    module_name, func_name = func_module_path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    func = getattr(mod, func_name)
    if not callable(func):
        raise ValueError("{0} is not a valid function module path.".format(
            func_module_path))

    # Decorate the function to type inputs/outputs
    decorated_func = returns(*output_arg_types)(inputs(*input_arg_types)(func))
    logger.debug("input types: {0}".format(decorated_func._input_types))
    logger.debug("output types: {0}".format(decorated_func._output_types))
    setattr(decorated_func, "_input_meta", input_meta)
    setattr(decorated_func, "_output_meta", output_meta)
    logger.debug("input meta: {0}".format(decorated_func._input_meta))
    logger.debug("output meta: {0}".format(decorated_func._output_meta))

    # Inspect the function to get input/output parameters
    prototype = inspect.getargspec(func)
    _inputs = prototype.args
    setattr(decorated_func, "_input_names", _inputs)
    logger.debug("inputs: {0}".format(decorated_func._input_names))
    defaults = dict(zip(reversed(prototype.args or []),
                        reversed(prototype.defaults or [])))
    setattr(decorated_func, "_default_values", defaults)
    logger.debug("defaults: {0}".format(decorated_func._default_values))
    code = inspect.getsourcelines(func)
    return_pattern = r"return\s*(.*)\n*$"
    _outputs = re.findall(return_pattern, code[0][-1])
    if len(_outputs) > 0:
        _outputs = [item.strip() for item in _outputs[0].split(",")]
    setattr(decorated_func, "_output_names", _outputs)
    logger.debug("outputs: {0}".format(decorated_func._output_names))
    logger.debug("Loading function done.")

    return decorated_func
