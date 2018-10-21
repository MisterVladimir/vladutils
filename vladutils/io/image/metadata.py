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
import json

from ...iteration import isiterable
from ..yaml import YAMLDict

UNIT_CONVERSION = {'microns': 'um', 'nanometers': 'nm',
                   'picometers': 'pm', 'µm': 'um', 'um': 'um',
                   'nm': 'nm', 'm': 'm'}


class MetaData(YAMLDict):
    """
    Stores image metadata as a nested dictionary.

    Parameters
    ------------
    raw : dict
        Metadata from image, as parsed by tifffile.TiffFile.
    """
    # metadata we need to keep
    _keys = ['Type', 'FileName', 'DimensionOrder', 'PhysicalSizeX',
             'PhysicalSizeXUnit', 'PhysicalSizeY', 'PhysicalSizeYUnit',
             'PhysicalSizeZ', 'PhysicalSizeZUnit',
             'SizeC', 'SizeT', 'SizeX', 'SizeY', 'SizeZ',
             'Creator']
    # rename units of measure
    unit_conversion = {'microns': 'um', 'nanometers': 'nm',
                       'picometers': 'pm', 'µm': 'um', 'um': 'um',
                       'nm': 'nm', 'm': 'm'}

    def __init__(self, raw):
        flat = self.__class__.flatten(raw)
        filtered = {k: v for k, v in flat.items() if k in self._keys}

        for key in filtered:
            if key.startswith('PhysicalSize') and key.endswith('Unit'):
                filtered[key] = self.unit_conversion[filtered[key]]
        try:
            x = filtered['PhysicalSizeX']
            xunit = filtered['PhysicalSizeXUnit']
            y = filtered['PhysicalSizeY']
            yunit = filtered['PhysicalSizeYUnit']
            if x == y and xunit == yunit:
                filtered['pixelsize'] = filtered['PhysicalSizeX']
                filtered['pixelunit'] = filtered['PhysicalSizeXUnit']
        except KeyError:
            filtered['pixelsize'] = None
            filtered['pixelunit'] = None

        super().__init__(filtered)

    def __missing__(self, name):
        return YAMLDict(__parent=self, __key=name)

    def to_JSON(self, **kwargs):
        return json.dumps(self, **kwargs)

    def save(self, path, **kwargs):
        """
        Save data as JSON file.
        """
        with open(path, 'a') as f:
            json.dump(self, f, **kwargs)
