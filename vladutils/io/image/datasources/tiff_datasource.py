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
import copy

from .base_datasource import BaseImageRequest, FileDataSource
from ....contrib.gohlke import tifffile


class TiffImageRequest(BaseImageRequest):
    __doc__ = BaseImageRequest.__doc__

    def _get_page_indices(self):
        """
        Converts data stored as key/value pairs in self to tiff page
        indices.
        """
        order = self.ctz_order
        # shape of the tif image, in its DimensionOrder
        tif_shape = np.array([self.image_shape[k] for k in order])

        # the requested index, stored as values in self, rearranged to the
        # DimensionOrder that the underlying tiff image data is in
        index = self[order]
        # which values in self are ints and which are slices
        from_ints = np.array([0 if isinstance(i, slice) else i
                              for i in index])[:, None]

        # check if any slice objects have been passed in
        # convert any slices to lists of integers
        is_slice = [isinstance(item, slice) for item in index]
        n_slice_objects = sum(is_slice)
        if n_slice_objects > 1:
            raise TypeError('Only one slice item may be present in the '
                            'request. {} were used.'.format(n_slice_objects))
        elif n_slice_objects == 0:
            # C, T, Z are already all integers and can be passed to
            # tifffile.TiffFile.asarray method.
            as_integers = from_ints
        else:
            # Convert slice objects to lists of integers.
            # If already integer, repeat the integer. 
            slice_index = np.flatnonzero(is_slice)[0]
            sl = index[slice_index]
            sliced_dim_length = tif_shape[slice_index]
            start, stop, step = sl.indices(sliced_dim_length)
            length = (stop - start) // step
            from_slices = [
                np.arange(start, stop, step) if isinstance(j, slice)
                else np.full(length, j, int) for j in zip(index)]
            as_integers = np.concatenate(from_slices).reshape((-1, length))
        # finally, identify the tif page data is in
        # throws ValueError if that CTZ combination is out of range
        page_indices = np.ravel_multi_index(as_integers, tif_shape)
        return page_indices

    def __call__(self, *ctzxy):
        """
        Returns the TiffPage index -- a list of indices if an argument is a
        slice object -- corresponding to the desired C, T, Z indices of a
        tiff image.
        """
        # keep an old copy to roll back in case of errors
        old_indices = copy.copy(self['CTZXY'])
        if len(ctzxy) == 5:
            self['CTZXY'] = ctzxy
        elif len(ctzxy) == 3:
            ctzxy = list(ctzxy) + [slice(None), slice(None)]
            self['CTZXY'] = ctzxy
        elif len(ctzxy) == 0:
            # use previous contents of self
            pass
        else:
            return None, None, None
        try:
            n = self._get_page_indices()
            return n, self['X'], self['Y']
        except (TypeError, IndexError) as e:
            # roll back to previous request
            if not len(ctzxy) == 0:
                self['CTZXY'] = old_indices
            raise e


class TiffDataSource(FileDataSource):
    """
    Reads a tiff file. Data corresponding to a given C, T, Z index can be
    retrieved without the user necessarily knowing the order the C, T, Z
    are stored in.

    Parameters
    -----------
    filename : str
        Full filename of the tiff image.

    request : BaseImageRequest subclass or list
        Each item in the list is a slice or int corresponding to the
        (channel, time, axial position) in that order.
    """

    module_name = 'tiff_datasource'

    def __init__(self, filename, request):
        super().__init__()
        self._request = request
        self.datasource = tifffile.TiffFile(filename)

    def request(self, *ctzxy):
        n, x, y = self._request(*ctzxy)
        im = self.datasource.asarray(key=n)
        if im.ndim == 2:
            im = im[None, :]
        return im[(slice(None), x, y)]

    def cleanup(self):
        self.datasource.close()
