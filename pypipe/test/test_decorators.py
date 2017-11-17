##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import unittest
import numpy

# Package import
from pypipe.demo import test1
from pypipe.lib.exceptions import ArgumentValidationError
from pypipe.lib.exceptions import InvalidArgumentNumberError
from pypipe.lib.exceptions import InvalidReturnType
from pypipe.lib.exceptions import InvalidReturnNumberError
from pypipe.lib.utils import inputs
from pypipe.lib.utils import returns


class TestDecorators(unittest.TestCase):
    """ Test function input/output parameters decorators.
    """

    def setUp(self):
        """ Initialize the TestDecorators class.
        """
        pass

    def test_raises(self):
        """ Method to test that the exceptions are raised properly.
        """
        # Return to new line
        print

        # Check raises
        decorated_func = inputs(str, float, int, str)(test1)
        self.assertRaises(
            InvalidArgumentNumberError, decorated_func, "a", 1.2, "5", "b", "c")
        decorated_func = inputs(str, float, int, str, str)(test1)
        self.assertRaises(
            ArgumentValidationError, decorated_func, "a", 1.2, "5", "b", "c")
        decorated_func = returns(int, int)(
            inputs(str, float, int, str, str)(test1))
        self.assertRaises(
            InvalidReturnNumberError, decorated_func, "a", 1.2, 5, "b", "c")
        decorated_func = returns(float)(
            inputs(str, float, int, str, str)(test1))
        self.assertRaises(
            InvalidReturnType, decorated_func, "a", 1.2, 5, "b", "c")


    def test_normal_exec(self):
        """ Method to test the normal exception.
        """
        decorated_func = returns(int)(
            inputs(str, float, int, str, str)(test1))
        exitcode = decorated_func("a", 1.2, 5, "b", "c")
        self.assertEqual(exitcode, 1)


    def test_string_decorators(self):
        """ Method to test the normal exception.
        """
        input_types = ("File", "Float", "Int", "Enum", "Str")
        output_types = ("Int", )
        decorated_func = returns(*output_types)(inputs(*input_types)(test1))
        exitcode = decorated_func("a", 1.2, 5, "b", i5="c")
        self.assertEqual(exitcode, 1)
        self.assertEqual(decorated_func._input_types, input_types)
        self.assertEqual(decorated_func._output_types, output_types)


def test():
    """ Function to execute unitests.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecorators)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
