##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines custom array rendering widgets.
"""

# System import
import numpy

# Third party import
import PySide
import pyqtgraph


def data_widget(data, scroll_axis=2):
    """ Plot an image associated data.
    Currently support on 1D, 2D or 3D data.

    Parameters
    ----------
    data: array
        the data to be displayed.
    scroll_axis: int (optional, default 2)
        the scroll axis for 3d data.

    Returns
    -------
    widget: Widget
        the generated widget.
    """
    # Check input parameters
    if data.ndim not in range(1, 4):
        raise ValueError("Unsupported data dimension.")

    # Deal with complex data
    if numpy.iscomplex(data).any():
        data = numpy.abs(data)

    # Create the widget
    if data.ndim == 3:
        indices = [i for i in range(3) if i != scroll_axis]
        indices = [scroll_axis] + indices
        widget = pyqtgraph.ImageView()
        widget.setImage(numpy.transpose(data, indices))
    elif data.ndim == 2:
        widget = pyqtgraph.ImageView()
        widget.setImage(data)
    else:
        widget = pyqtgraph.PlotWidget()
        widget.plot(data)

    return widget
