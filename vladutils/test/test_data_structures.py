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
from typing import Set
import unittest


from .. import data_structures as ds


class TrackedSetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.compare_to: Set[str] = set(('first', 'second', 'third'))
        self.li: ds.TrackedSet = ds.TrackedSet(self.compare_to)

    def test_add(self):
        self.assertSetEqual(self.li, self.compare_to)
        self.assertSetEqual(self.li.added, self.compare_to)
        self.assertSetEqual(self.li.removed, set())

    def test_remove(self):
        to_remove: str = 'first'
        self.compare_to.remove(to_remove)
        self.li.remove(to_remove)
        self.assertSetEqual(self.li, self.compare_to)
        self.assertSetEqual(self.li.removed, set((to_remove)))
        self.assertSetEqual(self.li.added, self.compare_to)

    def test_clear(self):
        self.li.clear()
        self.assertSetEqual(self.li, set())
        self.assertSetEqual(self.li.removed, self.compare_to)

    def test_difference_update(self):
        pass

    def test_discard(self):
        pass

    def test_intersection_update(self):
        pass

    def test_symmetric_difference_update(self):
        pass

    def test_pop(self):
        pass

    def test_update(self):
        pass



