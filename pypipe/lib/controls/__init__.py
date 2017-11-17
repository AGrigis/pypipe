##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines the controls.
"""

from .enum import Enum
from .file import File
from .directory import Directory
from .object import Object
from .string import String
from .int import Int
from .float import Float
from .list import List
from .base import Base


CONTROLS = {
    "Enum": Enum,
    "File": File,
    "Directory": Directory,
    "String": String,
    "Str": String,
    "Int": Int,
    "Float": Float,
    "Object": Object,
    "List": List,
}

