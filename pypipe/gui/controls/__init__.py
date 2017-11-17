##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines the controls widgets.
"""

from .enum import QtEnum
from .file import QtFile
from .directory import QtDirectory
from .string import QtString
from .int import QtInt
from .float import QtFloat
from .object import QtObjects
from .list import QtList


QTCONTROLS = {
    "Enum": QtEnum,
    "File": QtFile,
    "Directory": QtDirectory,
    "String": QtString,
    "Str": QtString,
    "Int": QtInt,
    "Float": QtFloat,
    "Objects": QtObjects,
    "List": QtList,
}
