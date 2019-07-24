##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import ast
import logging
from collections import OrderedDict

# Define the logger
logger = logging.getLogger(__name__)

# Package import
from pypipe.configure import info
from pypipe.apps.utils.window import MyQUiLoader
from pypipe.apps.utils.fill_treectrl import fill_treectrl
from pypipe.gui.controls import QTCONTROLS
from pypipe.gui.plotting import data_widget
from pypipe.gui.scroll_widgets import ScrollWidget
from pypipe.gui.function_widgets import FunctionDoc
from pypipe.gui.function_widgets import DeleteObjects
from pypipe.gui.function_widgets import FunctionParameters
from pypipe.lib.utils import load_func_from_module_path

# Third party import import
import numpy
from PySide2 import QtCore, QtWidgets


class PyPipeMainWindow(MyQUiLoader):
    """ PyPipe main window.
    """
    def __init__(self, menu, ui_file):
        """ Method to initialize the PyPipe main window class.

        Parameters
        ----------
        menu: hierachic dict
            each key is a sub module of the module. Leafs contain a list with
            the url to the documentation.
        ui_file: str (mandatory)
            a filename containing the user interface description
        default_study_config: ordered dict (madatory)
            some parameters for the study configuration
        """
        # Inheritance: load user interface window
        MyQUiLoader.__init__(self, ui_file)

        # Class parameters
        self.menu = menu
        self.functions = {}
        self._current_ui = None   
        self._current_del = None
        self._current_doc_html = None
        self._objects = []

        # Define dynamic controls
        self.controls = {
            QtWidgets.QAction: [
                "actionHelp", "actionQuit", "actionBrowse",
                "actionParameters", "actionDocumentation", "actionBoard"],
            QtWidgets.QTabWidget: [
                "display"],
            QtWidgets.QDockWidget: [
                "dockWidgetBrowse", "dockWidgetParameters", "dockWidgetDoc",
                "dockWidgetBoard"],
            QtWidgets.QWidget: [
                "dock_browse", "dock_parameters", "dock_doc",
                "dock_board"],
            QtWidgets.QTreeWidget: [
                "menu_treectrl"],
            QtWidgets.QLineEdit: [
                "search"],
        }

        # Add ui class parameter with the dynamic controls and initialize
        # default values
        self.add_controls_to_ui()
        self.ui.display.setTabsClosable(True)

        # Create the functions menu
        fill_treectrl(self.ui.menu_treectrl, self.menu)

        # Signal for window interface
        self.ui.actionHelp.triggered.connect(self.onHelpClicked)

        # Signal for tab widget
        self.ui.display.currentChanged.connect(self.onCurrentTabChanged)
        self.ui.display.tabCloseRequested.connect(self.onCloseTabClicked)

        # Signal for dock widget
        self.ui.actionBoard.triggered.connect(self.onBoardClicked)
        self.ui.actionBrowse.triggered.connect(self.onBrowseClicked)
        self.ui.actionParameters.triggered.connect(self.onParametersClicked)
        self.ui.actionDocumentation.triggered.connect(
            self.onDocumentationClicked)

        # Initialize properly the visibility of each dock widget
        self.onBoardClicked()
        self.onBrowseClicked()
        self.onParametersClicked()
        self.onDocumentationClicked()

        # Signal for function search and call
        self.ui.search.textChanged.connect(self.onSearchClicked)
        self.ui.menu_treectrl.currentItemChanged.connect(
            self.onTreeSelectionChanged)

        # Create objects managment widget
        self._on_update_widgets(None)

    def show(self):
        """ Shows the widget and its child widgets.
        """
        self.ui.show()

    def add_controls_to_ui(self):
        """ Method to find dynamic controls
        """
        # Error message template
        error_message = "{0} has no attribute '{1}'"

        # Got through the class dynamic controls
        for control_type, control_item in self.controls.items():

            # Get the dynamic control name
            for control_name in control_item:

                # Try to set the control value to the ui class parameter
                try:
                    value = self.ui.findChild(control_type, control_name)
                    if value is None:
                        logger.error(error_message.format(
                            type(self.ui), control_name))
                    setattr(self.ui, control_name, value)
                except:
                    logger.error(error_message.format(
                        type(self.ui), control_name))

    ###########################################################################
    # Slots   
    ###########################################################################

    def onBoardClicked(self):
        """ Event to show / hide the board dock widget.
        """
        # Show browse dock widget
        if self.ui.actionBoard.isChecked():
            self.ui.dockWidgetBoard.show()

        # Hide browse dock widget
        else:
            self.ui.dockWidgetBoard.hide()

    def onBrowseClicked(self):
        """ Event to show / hide the browse dock widget.
        """
        # Show browse dock widget
        if self.ui.actionBrowse.isChecked():
            self.ui.dockWidgetBrowse.show()

        # Hide browse dock widget
        else:
            self.ui.dockWidgetBrowse.hide()

    def onParametersClicked(self):
        """ Event to show / hide the parameters dock widget.
        """
        # Show parameters dock widget
        if self.ui.actionParameters.isChecked():
            self.ui.dockWidgetParameters.show()

        # Hide parameters dock widget
        else:
            self.ui.dockWidgetParameters.hide()

    def onDocumentationClicked(self):
        """ Event to show / hide the documentation dock widget.
        """
        # Show study configuration dock widget
        if self.ui.actionDocumentation.isChecked():
            self.ui.dockWidgetDoc.show()

        # Hide study configuration dock widget
        else:
            self.ui.dockWidgetDoc.hide()

    def onSearchClicked(self):
        """ Event to refresh the menu tree control that contains the pipeline
        modules.
        """
        # Clear the current tree control
        self.ui.menu_treectrl.clear()

        # Build the new filtered tree control
        fill_treectrl(self.ui.menu_treectrl, self.menu,
                      self.ui.search.text().lower())

    def onTreeSelectionChanged(self):
        """ Event to refresh the pipeline load button status.
        """
        # Get the cuurent item
        item = self.ui.menu_treectrl.currentItem()
        if item is None:
            return

        # Check if we have selected a function in the tree and enable / disable
        # the run button
        function_module_path = item.text(1)
        if function_module_path == "None":
            param_widget = self.ui.dockWidgetParameters.widget()
            if param_widget is not None:
                param_widget.close()
            doc_widget = self.ui.dockWidgetDoc.widget()
            if doc_widget is not None:
                doc_widget.close()
        else:
            # Create the function parameters widget
            function_input_params = [
                param if isinstance(param, (tuple, list)) else (param, {})
                for param in ast.literal_eval(item.text(2))]
            function_output_params = [
                param if isinstance(param, (tuple, list)) else (param, {})
                for param in ast.literal_eval(item.text(3))]
            self.ui.status.showMessage(
                "Loading '{0}'.".format(function_module_path))
            self.ui.status.reformat()
            self.ui.status.hideOrShow()
            function = load_func_from_module_path(
                func_module_path=function_module_path,
                input_arg_types=[param[0] for param in function_input_params],
                output_arg_types=[param[0] for param in function_output_params],
                input_meta=[param[1] for param in function_input_params],
                output_meta=[param[1] for param in function_output_params])
            self.ui.status.clearMessage()
            param_widget = FunctionParameters(
                function,
                objects=self._objects,
                status_widget=self.ui.status)
            param_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            param_widget.add_observer("update", self._on_update_widgets)
            scroll_param_widget = ScrollWidget(param_widget)
            scroll_param_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

            # Create the documentation widget
            doc_widget = FunctionDoc(function)
            doc_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

            # Add widgets to dock widgets
            self.ui.dockWidgetDoc.setWidget(doc_widget)
            self.ui.dockWidgetParameters.setWidget(scroll_param_widget)

    def onCloseTabClicked(self, index):
        """ Event to close a pipeline view.
        """
        # Remove the table
        self.ui.display.removeTab(index)
        

    def onCurrentTabChanged(self, index):
        """ Event to refresh the controller controller widget when a new
        tab is selected
        """
        # A new valid tab is selected
        if index >= 0:
            pass

    def onHelpClicked(self):
        """ Event to display the package information.
        """
        # Create a dialog box to display the package information
        win = QtWidgets.QDialog()
        win.setWindowTitle("PyPipe Help")
        QtWidgets.QMessageBox.information(self.ui, "Information", info())

    ###########################################################################
    # Private interface 
    ###########################################################################

    def _on_update_widgets(self, signal):
        """ Update all the widgets.

        This method is usefull for instance when the inner objects list
        is updated.

        Depending on the emited signal, all the objects with an array data
        element or the array objects will be displayed/removed.
        """
        # Process emited signal
        logger.debug("Update widgets::")
        if signal is not None:
            logger.debug("signal: {0} - {1} - {2}".format(
                signal.signal, signal.action, signal.position))

            # Close/add display in tab widget
            if signal.action in ["show", "add"]:
                new_object = self._objects[signal.position]
                if (hasattr(new_object, "data") and
                        isinstance(new_object.data, numpy.ndarray)):
                    display_widget = data_widget(new_object.data)
                elif isinstance(new_object, numpy.ndarray):
                    display_widget = data_widget(new_object)
                else:
                    display_widget = QtWidgets.QLabel()
                    display_widget.setText(repr(new_object))
                self._insert_widget_in_tab(display_widget, signal.position)
            elif signal.action == "del":
                self.ui.display.removeTab(signal.position)
                for idx in range(signal.position, self.ui.display.count()):
                    self.ui.display.setTabText(idx, str(idx))

        else:
            logger.debug("signal: None")
        logger.debug("objects: {0}".format(self._objects))

        # Close widgets in dock widgets
        self.ui.dockWidgetBoard.widget().close()
        scroll_param_widget = self.ui.dockWidgetParameters.widget()
        if scroll_param_widget is not None:
            scroll_param_widget.close()
        doc_widget = self.ui.dockWidgetDoc.widget()
        if doc_widget is not None:
            doc_widget.close()       

        # Create the object managment widget
        del_widgets = DeleteObjects(self._objects)
        del_widgets.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        del_widgets.add_observer("update", self._on_update_widgets)
        self.ui.dockWidgetBoard.setWidget(del_widgets)

        # Create the function parameters/documentation widgets
        self.onTreeSelectionChanged()
        logger.debug("Update widgets done.")

    def _insert_widget_in_tab(self, widget, index):
        """ Insert a new widget or replace an existing widget.

        Parameters
        ----------
        widget: a widget (mandatory)
            the widget we want to draw.
        index: int
            the tab index.
        """
        # Search if the tab corresponding to the widget has already been
        # created
        already_created = False
        idx = 0

        # Go through all the tabs
        for idx in range(self.ui.display.count()):

            # Check if we have a match: the tab name is equal to the current
            #pipeline name
            if (self.ui.display.tabText(idx) == str(index)):
                already_created = True
                break

        # If no match found, add a new tab with the widget
        if not already_created:
            self.ui.display.addTab(widget, str(index))
            self.ui.display.setCurrentIndex(self.ui.display.count() - 1)

        # Otherwise, replace the widget from the match tab
        else:
            # Delete the tab
            self.ui.display.removeTab(index)

            # Insert the new tab
            self.ui.display.insertTab(index, widget, str(index))

            # Set the corresponding index
            self.ui.display.setCurrentIndex(index)

