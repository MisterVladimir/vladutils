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
import copy
import pytest
import numpy as np

from vladutils import coordinate


@pytest.fixture
def coord():
    return coordinate.Coordinate(um=(5., 6))

def test_conversion(coord):
    assert all(coord['nm'])

def test_get_pixelsize(coord):
    assert coord.pixelsize is None
    coord['px'] = np.array((5, 6))
    assert all(coord.pixelsize)

def test_set_pixelsize_with_float(coord):
    # setting pixelsize to a number
    print(coord)
    coord.pixelsize = 100.
    assert all(coord['px'] == np.array([50, 60]))

def test_set_pixelsize_with_array(coord):
    coord.pixelsize = [20, 20]
    assert all(coord['px'] == np.array([250, 300]))

def test_set_pixelsize_with_coordinate(coord):
    coord.pixelsize = coordinate.Coordinate(nm=(50, 60))
    assert all(coord['px'] == np.array([100., 100.]))

def test_equal(coord):
    coord1 = copy.deepcopy(coord)
    coord2 = copy.deepcopy(coord)
    assert all(coord1 == coord2)
    assert coordinate.Coordinate(nm=1000.) == coordinate.Coordinate(um=1.)

def test_sum(coord):
    intended_result = coordinate.Coordinate(um=(7., 6.))
    start_coord = coord
    to_add = coordinate.Coordinate(um=(2., 0.))
    result = start_coord + to_add
    assert np.all(intended_result == result)

def test_mul(coord):
    intended_result = coordinate.Coordinate(um=(10., 12))
    start_coord = coord
    n = 2
    assert all(start_coord * n == intended_result)
    assert all(start_coord * np.array((n, n)) == intended_result)

def test_divide(coord):
    intended_result = coordinate.Coordinate(um=(2.5, 3.))
    start_coord = coord
    assert all(start_coord / 2. == intended_result)
    assert all(start_coord / [2., 2] == intended_result)
