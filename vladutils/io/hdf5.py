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
import h5py
import numpy as np
from collections import OrderedDict
from anytree import Node

__all__ = ['save_dict_to_hdf5', 'load_dict_from_hdf5']


# https://codereview.stackexchange.com/questions/120802/recursively-save-python-dictionaries-to-hdf5-files-using-h5py/121308
def save_dict_to_hdf5(dic, filename):
    """
    """
    with h5py.File(filename, 'w') as h5file:
        _recursively_save(h5file, '/', dic)


def _recursively_save(h5file, path, dic):
    """
    """
    for key, item in dic.items():
        if isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes)):
            h5file[path + key] = item
        elif isinstance(item, dict):
            _recursively_save(h5file, path + key + '/', item)
        else:
            pass


def load_dict_from_hdf5(filename):
    """
    """
    with h5py.File(filename, 'r') as h5file:
        return _recursively_load(h5file, '/')


def _recursively_load(grp, path):
    """
    """
    ans = OrderedDict()
    for key, item in grp[path].items():
        if isinstance(item, h5py.Dataset):
            ans[key] = item.value
        elif isinstance(item, h5py.Group):
            ans[key] = _recursively_load(grp, path + key + '/')
    return ans
