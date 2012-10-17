# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Andrew Colin Kissa <andrew@topdog.za.net>.
# Based on minify Copyright (c) 2011-2012 Sylvain Prat
# This program is open-source software, and may be redistributed
# under the terms of the MIT license. See the LICENSE file in this
# distribution for details
import os
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

required_packages = [
        "slimit",
        "cssmin",
        "scss",
    ]


def read(fname):
    "Read file and return contents"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_path(*path_parts):
    "Read files in a given path"
    here = os.path.dirname(__file__)
    return open(os.path.join(here, *path_parts)).read()


def find_version(*file_paths):
    "Read a version number"
    version_file = read_path(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='tsantsa',
    version=find_version('tsantsa', '__init__.py'),
    description='Tsantsa: CSS, JS minification and SCSS compilation commands for setuptools',
    long_description=read('README.rst'),
    author='Andrew Colin Kissa',
    author_email='andrew@topdog.za.net',
    url='http://www.topdog.za.net/tsantsa',
    install_requires=required_packages,
    packages=find_packages(exclude=['ez_setup']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Programming Language :: Python',
    ],
    entry_points = {
        'distutils.commands': [
            'tsantsa_js = tsantsa.minifer:tsantsa_js',
            'tsantsa_css = tsantsa.minifer:tsantsa_css',
            'compile_scss = tsantsa.scss_compiler:compile_scss',
        ]
    },
)
