# -*- coding: utf-8 -*-
"""
@author: Vladimir Shteyn
@email: vladimir.shteyn@googlemail.com

Copyright Vladimir Shteyn, 2018

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from collections import OrderedDict
from abc import abstractmethod

from ... import IO
from ....iteration import isiterable
from ....data_structures import IndexedDict


class BaseImageRequest(IndexedDict):
    """
    This class is meant to be used in conjunction with FileDataSource
    objects to return 2D or 3D images from a FileDataSource. Calling
    BaseImageRequest with the C, T, Z, X, Y indices should return
    parameters passed directly into the FileDataSource's 'request'
    method.

    This is a dictionary-like object that

        (1) stores the C, T, Z, X, and Y indices last retrieved from an
            image;
        (2) stores the dimension number of each of the above,
            C, T, Z, X, and Y;
        (3) offers convenient __setitem__ and __getitem__, as well as
            the iloc() method for setting and getting multiple key/value
            pairs with one call.

    Currently only 3-dimensional outputs are supported. That is, only one of
    the first three arguments to self.__call__() may be a slice object.

    Parameters
    -------------
    order : str
        Concatenated string of image dimension order.

    shape : iterable
        Shape of each image dimension in the order CTZXY.

    Example
    ---------
    # a 3-color image with 8 z slices, each slice 512x512
    req = TiffImageRequest('TCZXY', 3, 1, 8, 512, 512)
    datasource = TiffDataSource(image_path, req)

    # retrive image in the first channel, third timepoint, and all z slices
    # call the datasource's request method with arguments in C, T, Z order
    z_stack = datasource.request(0,2 , slice(None))
    """
    module_name = 'base_datasource'

    def __init__(self, order, *shape):
        # default starting values
        super().__init__(zip('CTZXY', [0, 0, 0, slice(None), slice(None)]))
        # TODO: make sure shape is 5 units long; otherwise, add 1s
        self.ctzxy_order = order.upper()
        self.ctz_order = self.ctzxy_order.replace('X', '').replace('Y', '')
        # shape of image data, in image's true dimension (channel, time, z)
        # order
        self.image_shape = IndexedDict(
            zip(self.ctzxy_order, [None]*len(self.ctzxy_order)))
        self.image_shape.update(dict(zip('CTZXY', shape)))

    def __setitem__(self, key, value):
        if isinstance(key, str) and isiterable(value):
            if len(key) == len(list(value)) > 1:
                for i, k in enumerate(key):
                    super().__setitem__(k, value[i])
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, str) and len(key) > 1:
            return [self.__getitem__(k) for k in key]
        else:
            return super().__getitem__(key)

    def __delitem__(self, key):
        raise NotImplementedError

    def __len__(self):
        return 5

    def insert(self, index, value):
        raise NotImplementedError('')

    @abstractmethod
    def __call__(self, *ctzxy):
        raise NotImplementedError('')


class FileDataSource(IO):
    """
    Abstract base class for pulling image data from a file.
    """
    module_name = 'base_datasource'

    @abstractmethod
    def request(self, *ctzxy):
        return NotImplemented


# TODO: untested
class NestedDataSource(IO):
    """
    Arguments
    -----------
    datasource: FileDataSource child class
    """
    module_name = 'base_datasource'

    def __init__(self, data):
        super().__init__()
        self.datasource = data
        # check that we have image data
        if not self.has_file_source(data):
            raise IOError('No image.')

    @staticmethod
    def has_file_source(ds):
        """
        Recursively check whether we have a sourcefile or other image
        dataset in the form of a numpy.ndarray.
        """
        if isinstance(ds, (FileDataSource, np.ndarray)):
            return True
        elif isinstance(ds, NestedDataSource):
            return ds.has_file_source(ds.datasource)
        else:
            return False

    @abstractmethod
    def request(self, *ctzxy):
        return NotImplemented

    def cleanup(self):
        self.datasource.cleanup()
