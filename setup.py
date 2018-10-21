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
from sys import platform
import os
from setuptools import setup, Extension
from numpy import get_include

with open('README.md', 'r') as f:
    README = f.read()


def get_requirements():
    with open('requirements.txt', 'r') as f:
        raw = f.read().replace(' ', '')
        return raw.split('\n')


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

if __name__ == '__main__':
    from setuptools import find_packages
    kwargs = [{'path_as_list': ['vladutils', 'contrib', 'gohlke'],
               'sources': ['psf.c'],
               'module_name': '_psf'},
              {'path_as_list': ['vladutils', 'contrib', 'gohlke'],
               'sources': ['tifffile.c'],
               'module_name': '_tifffile'}]
    ext = [create_extension(**k) for k in kwargs]
    ver = '0.1'
    url = r'https://github.com/MisterVladimir/vladutils'
    setup(name='vladutils',
          version=ver,
          packages=find_packages(),
          ext_modules=ext,
          python_requires='>=3.6',
          install_requires=get_requirements(),
          include_package_data=True,
          author='Vladimir Shteyn',
          author_email='vladimir.shteyn@googlemail.com',
          url=url,
          download_url=r'{0}/archive/{1}.tar.gz'.format(url, ver),
          long_description=README,
          license="GNUv3",
          classifiers=[
              'Intended Audience :: Science/Research',
              'Topic :: Scientific/Engineering :: Medical Science Apps.',
              'Topic :: Scientific/Engineering :: Image Recognition',
              'Programming Language :: Python :: 3.6'])
