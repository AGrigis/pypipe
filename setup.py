#! /usr/bin/env python
##########################################################################
# pypipe - Copyright (C) AGrigis, 2018
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


# System import
from __future__ import print_function
import os
import re
import sys
from pprint import pprint
from setuptools import setup, find_packages


# Package information
release_info = {}
infopath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "pypipe", "info.py"))
with open(infopath) as open_file:
    exec(open_file.read(), release_info)
pkgdata = {
    "pypipe": [
        os.path.join("apps", "resources", "*.png"),
        os.path.join("apps", "resources", "*.ui"),
        os.path.join("test", "*.py")]
}
if sys.version_info >= (3, 0):
    scripts = [
        os.path.join("pypipe", "apps", "pypipeview3")
    ]
else:
    scripts = [
        os.path.join("pypipe", "apps", "pypipeview")
    ]

# Workaround
if "--release" in sys.argv:
    sys.argv.remove("--release")
    scripts = [
        os.path.join("pypipe", "apps", "pypipeview3"),
        os.path.join("pypipe", "apps", "pypipeview")
    ]


# Write setup
setup(
    name=release_info["NAME"],
    description=release_info["DESCRIPTION"],
    long_description=release_info["LONG_DESCRIPTION"],
    license=release_info["LICENSE"],
    classifiers=release_info["CLASSIFIERS"],
    author=release_info["AUTHOR"],
    author_email=release_info["AUTHOR_EMAIL"],
    version=release_info["VERSION"],
    url=release_info["URL"],
    packages=find_packages(exclude="doc"),
    platforms=release_info["PLATFORMS"],
    extras_require=release_info["EXTRA_REQUIRES"],
    install_requires=release_info["REQUIRES"],
    package_data=pkgdata,
    scripts=scripts
)
