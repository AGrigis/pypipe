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
from pypipe.lib.controls import Base
from pypipe.lib.controls import File
from pypipe.lib.controls import Directory
from pypipe.lib.controls import String
from pypipe.lib.controls import Enum
from pypipe.lib.controls import Int
from pypipe.lib.controls import Float
from pypipe.lib.controls import Object
from pypipe.lib.controls import List


class TestControls(unittest.TestCase):
    """ Test observable pattern.
    """

    def setUp(self):
        """ Initialize the TestControls class.
        """
        self.path = os.path.abspath(__file__)
        self.dirname = os.path.dirname(self.path)
        self.word = "hello"
        self.choices = ("c1", "c2", "c3")
        self.array = numpy.array([10, 10])
        self.file = File(self.path, crazy=True, optional=True)
        self.dir = Directory(self.dirname, crazy=True, optional=True)
        self.string = String(self.word, crazy=True, optional=True)
        self.enum = Enum(choices=self.choices)
        self.object = Object(self.array)
        self.list = List([["a", "b"], ["c"]], content="List_String")
        self.int = Int()
        self.float = Float()

    def test_base(self):
        """ Method to test if the base parameter is correctly defined.
        """
        # Return to new line
        print

        # Check raises
        self.assertRaises(NotImplementedError, Base)
        self.assertRaises(ValueError, self.string._update_value, object())

    def test_directory(self):
        """ Method to test if the directory parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertEqual(self.dir.value, self.dirname)
        self.assertEqual(self.dir.crazy, True)
        self.assertEqual(self.dir.type, None)
        self.assertEqual(self.dir.optional, True)

        # Update parameter with a wrong value
        self.dir.value = ""
        self.assertEqual(self.dir.value, self.dirname)

        # Update parameter with undefined value
        self.dir.value = None
        self.assertEqual(self.dir.value, None)

    def test_string(self):
        """ Method to test if the string parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertEqual(self.string.value, self.word)
        self.assertEqual(self.string.crazy, True)
        self.assertEqual(self.string.type, None)
        self.assertEqual(self.string.optional, True)

        # Update parameter with a wrong value
        self.string.value = 10
        self.assertEqual(self.string.value, self.word)

        # Update parameter with undefined value
        self.string.value = None
        self.assertEqual(self.string.value, None)

    def test_enum(self):
        """ Method to test if the enum parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertEqual(self.enum.value, None)
        self.enum.value = "c1"
        self.assertEqual(self.enum.value, "c1")
        self.enum.value = None

        # Update parameter with a wrong value
        self.enum.value = "bad"
        self.assertEqual(self.enum.value, None)

        # Create parameter with wrong type: destroy current object for demo
        self.enum.choices = list(self.choices)
        self.assertRaises(Exception, self.enum._is_valid, self.enum.value)
        delattr(self.enum, "choices")
        self.assertRaises(Exception, self.enum._is_valid, self.enum.value)

    def test_list(self):
        """ Method to test if the list parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertFalse(self.list.inner)
        self.assertTrue(self.list.inner_control.inner)
        self.assertEqual(self.list.value, [["a", "b"], ["c"]])
        self.list.value = None
        self.assertEqual(self.list.value, None)
        self.list.value = [["a", 2], ["c"]]
        self.assertEqual(self.list.value, None)
        self.list.value = (["a", 2], ["c"])
        self.assertEqual(self.list.value, None)

        # Test raised cases
        self.assertRaises(ValueError, List)
        self.assertRaises(ValueError, List, content="Bad")

    def test_object(self):
        """ Method to test if the object parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertTrue(numpy.allclose(self.object.value, self.array))

    def test_int(self):
        """ Method to test if the integer parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertEqual(self.int.value, None)
        self.int.value = 15
        self.assertEqual(self.int.value, 15)
        self.int.value = 17.
        self.int.value = "bad"
        self.assertEqual(self.int.value, 15)

    def test_float(self):
        """ Method to test if the float parameter is correctly defined.
        """
        # Return to new line
        print

        # Check parameter state
        self.assertEqual(self.float.value, None)
        self.float.value = 15.
        self.assertEqual(self.float.value, 15.)
        self.float.value = 17
        self.float.value = "bad"
        self.assertEqual(self.float.value, 15.)


def test():
    """ Function to execute unitests.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestControls)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
