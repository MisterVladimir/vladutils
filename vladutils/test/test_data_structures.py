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
from typing import Set

from vladutils import data_structures as ds


ARG = ('first', 'second', 'third')


@pytest.fixture
def test_set():
    return set(ARG)

@pytest.fixture
def test_tracked_set():
    return ds.TrackedSet(ARG)


def test_add(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    assert test_set == test_tracked_set
    assert test_set == test_tracked_set.added
    assert set() == test_tracked_set.removed

def test_remove(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    to_remove: str = 'first'
    test_set.remove(to_remove)
    test_tracked_set.remove(to_remove)
    assert test_set == test_tracked_set
    assert set() == test_tracked_set.removed
    assert test_set == test_tracked_set.added

def test_clear(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    test_tracked_set.clear()
    assert test_tracked_set == set()
    assert test_tracked_set.removed == test_set

def test_difference_update(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass

def test_discard(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass

def test_intersection_update(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass

def test_symmetric_difference_update(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass

def test_pop(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass

def test_update(test_set: Set[str], test_tracked_set: Set[str]) -> None:
    pass
