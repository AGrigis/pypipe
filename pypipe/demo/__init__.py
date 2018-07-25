##########################################################################
# PyPipe - Copyright (C) AGrigis, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that defines demonstration function.
"""

# System import
from __future__ import print_function
import os


def test1(i1, i2, i3="a", i4=None, i5="", i6="test"):
    """
    Test function 1.

    Parameters
    ----------
    i1: str
        a valid file path.
    i2: float
        a float value.
    i3: int
        an integer value.
    i4: str
        a string.
    i5: object
        a Python object.
    i6: str
        a string.

    Returns
    -------
    r1: int
        the exitcode.
    """
    r1 = 0
    if not os.path.isfile(i1):
        print("{0} is not a valid file.".format(i1))
        r1 = 1
    if not isinstance(i2, float):
        print("{0} is not a valid float.".format(i2))
        r1 = 1
    if not isinstance(i3, int):
        print("{0} is not a valid integer.".format(i3))
        r1 = 1
    for param in (i4, i5):
        if not isinstance(param, unicode):
            print("{0} is not a valid string.".format(param))
            r1 = 1
    return r1


def generate_data(ndim=2):
    """
    Generate a toy dataset

    Parameters
    ----------
    ndim: int, default 2
        the output array dimension.

    Returns
    -------
    data: array
        the generated array.
    """
    import numpy
    pixels = [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]]
    pixels.append([0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0])
    pixels.append([0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0])
    pixels.append([0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0])
    pixels.append([0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0])
    pixels.append([1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1])
    pixels.append([1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1])
    pixels.append([1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1])
    pixels.append([1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1])
    pixels.append([1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1])
    pixels.append([1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1])
    pixels.append([1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1])
    pixels.append([0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0])
    pixels.append([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    pixels.append([0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0])
    pixels.append([0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])
    data = numpy.asarray(pixels).T
    if ndim not in (2, 3):
        raise ValueError("Unsupported dimension.")
    if ndim == 3:
        data.shape += (1, )
        data = numpy.concatenate((data, data * 5, data * 10), axis=-1)
    return data


def histogram(data, nbins=256, lower_cut=0., cumulate=0):
    """
    Compute the histogram of an input dataset.

    Parameters
    ----------
    data: array
        the dataset to be analysed.
    nbins: int, default 256
        the histogram number of bins.
    lower_cut: float, default 0
        do not consider the intensities under this threshold.
    cumulate: bool, default False
        if set compute the cumulate histogram.

    Returns
    -------
    hist_im: Image
        the generated histogram.
    """
    import numpy
    hist, bins = numpy.histogram(data[data > lower_cut], nbins)
    if cumulate:
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        hist_im = cdf_normalized
    else:
        hist_im = hist
    return hist_im



