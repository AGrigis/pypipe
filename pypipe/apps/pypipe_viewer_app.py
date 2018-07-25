##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import json
import logging

# Define the logger
logger = logging.getLogger(__name__)

# Package import
from pypipe.apps.utils.application import Application
from pypipe.apps.main_window import PyPipeMainWindow
import pypipe.apps.resources as resources


class PyPipeViewerApp(Application):
    """ PyPipe Viewer Application.
    """
    # Load some meta informations
    from pypipe.info import __version__ as _version
    from pypipe.info import NAME as _application_name
    from pypipe.info import ORGANISATION as _organisation_name

    def __init__(self, *args, **kwargs):
        """ Method to initialize the PyPipeViewerApp class.
        """
        # Inhetritance
        super(PyPipeViewerApp, self).__init__(*args, **kwargs)

        # Initialize the application
        self.window = None
        self.init_window()

    def init_window(self):
        """ Method to initialize the main window.
        """
        # First set some meta informations
        self.setApplicationName(self._application_name)
        self.setOrganizationName(self._organisation_name)
        self.setApplicationVersion(self._version)

        # Get the user interface description from package resources
        ui_file = os.path.join(resources.__path__[0], "pypipe.ui")

        # List declared functions.
        if self.options.test:
            menu = {
                "pypipe": {
                    "demo": {
                        "test1": [
                            "pypipe.demo.test1",
                            ("File", "Float", "Int", ("Enum", {"choices":
                             ("choice1", "choice2")}), ("Objects",
                             {"otype": "list"}), "Str"),
                            (("Objects", {"otype": "int"}), )
                        ],
                        "load": [
                            "pypipe.demo.generate_data",
                            ("Int", ),

                            (("Objects", {"otype": "ndarray"}), )
                        ],
                        "plotting": {
                            "histogram": [
                                "pypipe.demo.histogram",
                                [["Objects", {"otype": "ndarray"}], "Int",
                                  "Float", "Int"],
                                [["Objects", {"otype": "ndarray"}]]
                            ]
                        }
                    }
                }
            }
        else:
            if self.options.config is not None:
                with open(self.options.config, "rt") as open_file:
                    menu = json.load(open_file)
            else:
                menu = {}

        # Create and show the main window
        self.window = PyPipeMainWindow(menu, ui_file)
        self.window.show()
        self.window.ui.status.showMessage("Ready", 4000)

        return True

