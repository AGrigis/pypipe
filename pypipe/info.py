##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" 
This file defines project global parameters that are shared for instance with
the package setup.
"""

# Module current version
version_major = 0
version_minor = 0
version_micro = 1

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)

# Expected by setup.py: the status of the project
CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: BSD License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Project descriptions
description = """
PyPipe is a Python package that provides an easy to use user graphical
interface to pipe processings from different processing packages.
"""
long_description = """
======
PyPipe
======

PyPipe is a Python package that provides an easy to use user graphical
interface to pipe processings from different processing packages.

* Functions exposed in the user graphical interface are defined in a
configuration file.
"""

# versions for dependencies
PYSIDE_MIN_VERSION = "1.2.2"

# Main setup parameters
NAME = "PyPipe"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/AGrigis/pypipe"
DOWNLOAD_URL = "https://github.com/AGrigis/pypipe"
LICENSE = "CeCILL-B"
ORGANISATION = ""
CLASSIFIERS = CLASSIFIERS
AUTHOR = "Antoine Grigis <antoine.grigis@cea.fr>"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
ISRELEASE = True
VERSION = __version__
PROVIDES = ["pypipe"]
REQUIRES = ["PySide>={0}".format(PYSIDE_MIN_VERSION) ]
EXTRA_REQUIRES = {}
