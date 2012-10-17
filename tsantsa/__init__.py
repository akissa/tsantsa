# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Andrew Colin Kissa <andrew@topdog.za.net>.
# Based on minify Copyright (c) 2011-2012 Sylvain Prat
# This program is open-source software, and may be redistributed
# under the terms of the MIT license. See the LICENSE file in this
# distribution for details
"""
Tsantsa - CSS and JS minification plugin for setup tools
"""
__version__ = '0.0.1'
__author__ = "Andrew Colin Kissa"
__copyright__ = "Copyright 2012 Andrew Colin Kissa"
__email__ = "andrew@topdog.za.net"

import os
import glob
import tempfile

from distutils.cmd import Command


def remove_duplicates(lst):
    """
    Utility function to remove duplicates from a list while preserving the
    order of the elements
    """
    seen = set()
    seen_add = seen.add
    return [item for item in lst if item not in seen and not seen_add(item)]


class TsantsaBaseCmd(Command):
    """tsantsa base class"""

    user_options = [
        ('sources=', None, 'sources files'),
        ('output=', None, 'compiled css output file'),
    ]

    def initialize_options(self):
        """init options"""
        self.sources = None
        self.output = None

    @staticmethod
    def _files_list(path_specs):
        "Glob for file names"
        return [item for path in path_specs for item in glob.glob(path)]

    @staticmethod
    def _create_temporary_file():
        "Create a temp file"
        handle, path = tempfile.mkstemp(prefix='tsantsa')
        os.close(handle)
        return path

    @staticmethod
    def _combine_files(input_files, output_file):
        """Combine the input files to a big output file"""
        with open(output_file, mode='wb') as out:
            for input_file in input_files:
                out.write(open(input_file, mode='rb').read())
