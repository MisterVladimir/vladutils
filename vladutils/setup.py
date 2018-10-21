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
import os
from sys import platform
from setuptools import Extension
from numpy import get_include


def create_extension(path_as_list, sources, module_name):
    # def create_extension(name, sources):
    """
    """
    if platform == 'darwin':
        # MacOS
        link_args = []
    else:
        link_args = ['-static-libgcc']

    compile_args = ['-O3', '-fno-exceptions', '-ffast-math',
                    '-march=nocona', '-mtune=nocona']

    parent_directory = os.path.sep.join(path_as_list)
    sources = [os.path.join(parent_directory, s) for s in sources]
    name = os.path.extsep.join(path_as_list + [module_name])

    return Extension(name, sources, include_dirs=[get_include()],
                     extra_compile_args=compile_args,
                     extra_link_args=link_args)
