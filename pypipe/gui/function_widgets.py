##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import textwrap
import logging
import traceback

# Package import
from pypipe.lib.base import Observable
from pypipe.gui.controls import QTCONTROLS

# Third party import
from docutils.core import publish_string, publish_parts
from PySide import QtGui, QtCore, QtWebKit


# Create a logger
logger = logging.getLogger(__name__)


class FunctionDoc(QtGui.QWidget) :
    """ Generate function documentation widget from its rst docstring.
    """
    def __init__(self, function):
        """Initialize the 'FunctionDoc' class.

        Parameters
        ----------
        function: callable
            the function to document.
        """
        # Inheritance
        super(FunctionDoc, self).__init__()  

        # Get the docstring
        self._doc = textwrap.dedent(function.__doc__)
        self.doc_html = publish_string(self._doc, writer_name="html")

        # Display the html documentation
        self._layout = QtGui.QVBoxLayout()
        self._text = QtWebKit.QWebView() 
        self._text.setHtml(self.doc_html)
        self._text.show()
        self._layout.addWidget(self._text)
        self.setLayout(self._layout)


class FunctionParameters(QtGui.QWidget, Observable):
    """ Generate function parameters widget.
    """  
    def __init__(self, function, objects=None, status_widget=None):
        """ Initialize the 'FunctionParameters' class.

        Emit an 'update' signal when the widget is updated.

        Parameters
        ----------
        function: callable
            the function to execute.
        objects: list, default None
            if an Objects control is created use this container.
        status_widget: Widget, default None
            a status widget to display inforamtion to the user.
        """
        # Inheritance
        Observable.__init__(self, ["update"])
        super(FunctionParameters, self).__init__()   
 
        # Define the class attibutes
        self._controls = {}
        self._objects = objects
        self._function = function
        self._status = status_widget

        # Define the widget main layout
        self._layout = QtGui.QVBoxLayout()
        self._grid = QtGui.QGridLayout()
        self._init_ui()
        self.setLayout(self._layout)

        # Define signals
        self._run.clicked.connect(self.onrun)
        self._reset.clicked.connect(self.onreset)
    
    def __call__(self):
        """ Method to execute the function.
        """            
        # Build function expression and namespace
        namespace, expression = self._build_expression()

        # Display message to user
        self._status.showMessage("Running {0}".format(repr(self._function)))  
        self._status.reformat()
        self._status.hideOrShow()
     
        # Execute it
        logger.debug("Execute function::")
        logger.debug(expression)
        def f():
            exec expression in namespace  
        f()
        logger.debug("Execute function done.")

        # Update values
        update_interface = False
        logger.debug("Function outputs::")
        for name, control in self._controls.items():
            if control.is_output:
                logger.debug("{0}: {1}".format(name, namespace[name]))
                update_interface = True
                if control.type == "Objects":
                    object_id = control._current_object
                    if object_id is None:
                        self._objects.append(namespace[name])
                        object_id = len(self._objects) - 1
                    else:  
                        self._objects[object_id] = namespace[name]
                else:
                    object_id = None
                    control.value = namespace[name]
        logger.debug("objects: {0}".format(self._objects))
        logger.debug("Function outputs done.")

        # Update interface
        if update_interface and object_id is not None:
            self.notify_observers("update", action="add", position=object_id)

        # Done
        self._status.clearMessage()

    def validate_form(self):
        """ Method that checks if all the controls are defined properly.
        """
        all_controls_valid = True
        logger.debug("Validation status::")
        for name, control in self._controls.items():
            if control.is_output:
                continue
            logger.debug("{0}: {1} (optional {2}, value {3})".format(
                name, control.valid, control.is_optional, control.value))
            all_controls_valid = (all_controls_valid and control.valid)
            if not all_controls_valid:
                break
        logger.debug("Validation status done.")
        self._run.setEnabled(all_controls_valid)
    
    #######################################################################
    # Properties
    #######################################################################
    
    def _get_controls(self):
        return self._controls
    
    controls = property(_get_controls)
    
    #######################################################################
    # Signals 
    #######################################################################

    def onrun(self):
        """ Event to execute the function.
        """
        # Deactivate buttons
        self._run.setEnabled(False)
        self._reset.setEnabled(False)

        # Execute function
        self()

        # Activate buttons
        self._run.setEnabled(True)
        self._reset.setEnabled(True)
        
    def onreset(self) :
        """ Event to reset the function displayed parameters.
        """
        for name, control in self._controls.items():
            control.reset()
        self.validate_form()
       
    #######################################################################
    # Private interface 
    #######################################################################

    def _build_expression(self):
        """ Method that build the function expression and namespace.

        Returns
        -------
        namespace: dict
            the function exec namespace.
        expression: str
            the function exec expression.
        """
        # Build the function namespace
        namespace = {"function" : self._function}
        for name, control in self._controls.items():
            if control.is_output:
                namespace[name] = None
            else:
                namespace[name] = control.value
       
        # Build the function expression
        args = []
        return_values = []
        for name, control in self._controls.items():
            if control.is_output:
                return_values.append(name)
            else :
                args.append("{0}={0}".format(name))
        expression = "function({0})".format(", ".join(args))
        if return_values : 
            return_expression = ", ".join(return_values)
            expression = "{0} = {1}".format(return_expression, expression)

        return namespace, expression

    def _on_value_changed(self, signal):
        """ Callback used when the value of a control has changed.
        """
        self.validate_form()
    
    def _init_ui(self):
        """ Define the user interface.
        """
        # Update layout
        self._layout.setSpacing(5)
        self._layout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self._layout.setContentsMargins(10, 0, 0, 0)

        # Auto controls
        cnt = 0
        for param_names, is_output in (
                (self._function._input_names, False),
                (self._function._output_names, True)):
            for idx, pname in enumerate(param_names):

                # Create the parameter control widget
                logger.debug("Create control::")
                logger.debug("name: {0}".format(pname))   
                logger.debug("output: {0}".format(is_output))               
                if is_output:
                    ptype = self._function._output_types[idx]
                else:
                    ptype = self._function._input_types[idx]
                logger.debug("type: {0}".format(ptype))   
                if ptype not in QTCONTROLS:
                    raise ValueError(
                        "Unrecognize control '{0}'.".format(ptype))
                args = []
                if is_output:
                    kwargs = self._function._output_meta[idx].copy()
                else:
                    kwargs = self._function._input_meta[idx].copy()
                kwargs["name"] = pname
                kwargs["is_output"] = is_output
                kwargs["type"] = ptype
                if ptype == "Objects":
                    if self._objects is None:
                        raise ValueError("Please specify the container for "
                                         "the 'Objects' widget.")
                    args.append(self._objects)
                if pname in self._function._default_values:
                    kwargs["is_optional"] = True
                    kwargs["value"] = self._function._default_values[pname]
                try:
                    control = QTCONTROLS[ptype](*args, **kwargs)
                except:
                    trace = traceback.print_exc()
                    raise ValueError(
                        "{0}\nImpossible to build control '{1}' of type '{2}' "
                        "with the provided parameters '{3}'.".format(
                            trace, pname, ptype, kwargs))
                self._controls[pname] = control

                # Add observer
                control.add_observer("value", self._on_value_changed)
                logger.debug("Create control done.")

                # Add input controls to the grid widget
                if not control.is_output:
                    self._grid.addWidget(QtGui.QLabel(pname), 2 * cnt, 0)
                    self._grid.addWidget(control, 2 * cnt + 1, 0)
                    cnt += 1

        # Run & reset buttons
        self._run = QtGui.QPushButton("Run", self)
        self._reset = QtGui.QPushButton("Reset", self)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self._run)
        hbox.addWidget(self._reset)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # Add Layout
        self._layout.addLayout(self._grid)
        self._layout.addLayout(vbox)     

        # Check the form after initialization
        self._on_value_changed(None)


class DeleteObjects(QtGui.QWidget, Observable):
    """ Generate a widget to remove objects and notify observers.
    """
    def __init__(self, objects):
        """ Initialize the 'DeleteObjects' class.

        Parameters
        ----------
        objects: list
            the objects to be managed.
        """
        # Class attributes
        self._objects = objects

        # Inheritance
        Observable.__init__(self, ["update"])
        super(DeleteObjects, self).__init__() 

        # Define the widget layout
        self._layout = QtGui.QVBoxLayout()
        self._init_ui()
        self.setLayout(self._layout) 
        self.validate_form() 
 
    def _init_ui(self):
        """ Define the user interface.
        """
        # Add the control to the layout
        self.control = QTCONTROLS["Objects"](self._objects, name="manager")
        self.control.add_observer("value", self._on_value_changed)
        self._layout.addWidget(self.control)  

        # Add a delete button to the layout
        frame  = QtGui.QFrame()
        frame_layout = QtGui.QHBoxLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignLeft)
        self._del = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/delete"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self._del.setIcon(icon)
        self._del.setIconSize(QtCore.QSize(24, 24))
        self._del.setObjectName("delete_obj_icon")
        self._del.clicked.connect(self.on_del_clicked)
        frame_layout.addWidget(self._del)

        # Add a show button to the layout
        self._show = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/add"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._show.setIcon(icon)
        self._show.setIconSize(QtCore.QSize(24, 24))
        self._show.setObjectName("delete_obj_icon")
        self._show.clicked.connect(self.on_show_clicked)
        frame_layout.addWidget(self._show)
        frame.setLayout(frame_layout)
        self._layout.addWidget(frame)

    def validate_form(self):
        """ Method that checks if all the controls are defined properly.
        """
        all_controls_valid = self.control.valid  
        self._del.setEnabled(all_controls_valid)
        self._show.setEnabled(all_controls_valid)

    #######################################################################
    # Signals 
    #######################################################################

    def _on_value_changed(self, signal):
        """ Enable/disable the delete button when the control value is updated.
        """
        self.validate_form()   

    def on_del_clicked(self) :
        """ Remove the selected object from the list and notify observers
        with the 'update' signal.
        """
        del self._objects[self.control._current_object]
        self.notify_observers("update", action="del",
                              position=self.control._current_object)

    def on_show_clicked(self) :
        """ Notify observers an object want to be displayed with the 'update'
        signal.
        """
        self.notify_observers("update", action="show",
                              position=self.control._current_object)

