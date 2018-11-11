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
from addict import Dict as _Dict
import sys
from ruamel import yaml
import numpy as np
import copy
from operator import xor

from .iteration import isiterable


def print_nested_dict(dic, depth=0, prepend='\t'):
    for k, v in dic.items():
        if hasattr(v, 'keys'):
            print('{}{}'.format(depth * prepend, k))
            print_nested_dict(v, depth + 1, prepend=prepend)
        else:
            print('{}{}: {}'.format(depth * prepend, k, v))


class Dict(_Dict):
    @classmethod
    def flatten(cls, dic):
        """
        Returns the leaf dictionaries in the nested dictionary, 'dic'. If the value of a
        node is a dictionary whose value is (1) an iterable e.g. a list or
        tuple and (2) all items in the iterable are dictionaries, check
        whether the dictionaries are leaves.
        """
        def _flatten(_dic, _key):
            if isinstance(_dic, dict):
                for k, v in _dic.items():
                    _flatten(v, k)
            elif isiterable(_dic):
                # check if the iterable contains all dicts
                if all([isinstance(i, dict) for i in _dic]):
                    # if so, flatten the contained dictionaries
                    for item in _dic:
                        _flatten(item, _key)
                else:
                    # otherwise, this iterable is a leaf
                    ret.update({_key: _dic})
            else:
                # base case
                # in previous call to flatten, we iterated through 
                ret.update({_key: _dic})
        ret = {}
        _flatten(dic, None)
        return ret


class IndexedDict(dict):
    """
    Allows setting and getting keys/values by passing in the key index.

    We cannot use an integer key to set a value to None. The workaround is to
    use a key of type slice and an iterable containing None:
    >>> d = IndexedDict()
    >>> d['a'] = 0
    >>> d.iloc(slice(1), [None])
    >>> d
    {'a': None}
    """
    def _get_with_int(self, key, value):
        return self[key]

    def _get_with_slice(self, key, value):
        return [self[k] for k in key]

    def _set_with_int(self, key, value):
        self[key] = value

    def _set_with_slice(self, key, value):
        for k, v in zip(key, value):
            self[k] = v

    def iloc(self, i, value=None):
        try:
            keys = list(self.keys())[i]
        except IndexError as e:
            raise KeyError('Key must be set via self.__setitem__ before '
                           'referencing it via the .iloc() method.') from e
        else:
            method_dict = {(True, False): self._get_with_int,
                           (True, True): self._get_with_slice,
                           (False, False): self._set_with_int,
                           (False, True): self._set_with_slice}

            if xor(isiterable(keys), isiterable(value)):
                raise TypeError('Cannot set an iterable value with '
                                'non-iterable key and vice versa.')

            method = method_dict[
                (value is None, isiterable(keys) and isiterable(value))]
            return method(keys, value)


class TrackedSet(set):
    """
    Set that keeps track of items added and removed.
    """
    def __init__(self, iterable=None):
        self.removed = set()
        self.added = set()
        if iterable:
            super().__init__(iterable)
            self._add_addable(iterable)
        else:
            super().__init__()

    def _refresh(self):
        temp = copy.copy(self.added)
        self.added.difference_update(self.removed)
        self.removed.difference_update(temp)

    def _add_removeable(self, item):
        if isiterable(item):
            self.removed.update(item)
        else:
            self.removed.add(item)
        self._refresh()

    def _add_addable(self, item):
        if isiterable(item):
            self.added.update(item)
        else:
            self.added.add(item)
        self._refresh()

    def clear(self):
        self.removed.update(self)
        super().clear()

    def remove(self, item):
        super().remove(item)
        self._add_removeable(item)

    def difference_update(self, other):
        other = set(other)
        self._add_removeable(self.intersection(other))
        super().difference_update(other)

    def discard(self, other):
        if other in self:
            self._add_removeable(other)
            super().discard(other)

    def intersection_update(self, other):
        other = set(other)
        self._add_removeable(self.difference(other))
        super().intersection_update(other)

    def symmetric_difference_update(self, other):
        other = set(other)
        self._add_removeable(self.intersection(other))
        add = other.difference(self)
        self._add_addable(add)
        super().symmetric_difference_update(other)

    def pop(self):
        ret = super().pop()
        self._add_removeable(ret)
        return ret

    def update(self, other):
        self._add_addable(other)
        super().update(other)

    def add(self, other):
        self._add_addable(other)
        super().add(other)
