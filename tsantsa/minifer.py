# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Andrew Colin Kissa <andrew@topdog.za.net>.
# Based on minify Copyright (c) 2011-2012 Sylvain Prat
# This program is open-source software, and may be redistributed
# under the terms of the MIT license. See the LICENSE file in this
# distribution for details
"""
Tsantsa - CSS and JS minification plugin for setup tools
"""
import os

import cssmin

from slimit import minify
from tsantsa import TsantsaBaseCmd, remove_duplicates

def do_slimit(input_file, output_file, mangle):
    """
    Minify js using slimit
    """
    with open(output_file, mode='wb') as out:
        out.write(
            minify(open(input_file, mode='rb').read(), mangle=mangle)
        )

def do_cssmin(input_file, output_file):
    """
    Minify css using cssmin
    """
    with open(output_file, mode='wb') as out:
        out.write(cssmin.cssmin(open(input_file, mode='rb').read()))


class TsantsaCmd(TsantsaBaseCmd):
    """tsantsa setuptools command"""
    minification_type = 'js'

    user_options = [
        ('sources=', None, 'sources files'),
        ('output=', None, 'minified output filename. If you provide a template'
                          ' output filename (e.g. "static/%s-min.ext"), the'
                          ' source files will be minified individually'),
    ]

    boolean_options = []

    def finalize_options(self):
        """finalize options"""
        clean_path = os.path.normcase
        default_output = 'min.%s' % self.minification_type
        self.ensure_string('output', default_output)
        self.output = clean_path(self.output)
        self.ensure_string_list('sources')
        if self.sources:
            self.sources = remove_duplicates(clean_path(path)
                            for path in self._files_list(self.sources))

    def _minify_operation(self, sources, output):
        """Run a minification operation on the sources"""
        try:
            input_file = sources.pop()
            if len(sources) > 1:
                combined_filename = self._create_temporary_file()
                self._combine_files(sources, combined_filename)
                input_file = combined_filename

            if self.minification_type == 'css':
                do_cssmin(input_file, output)
            else:
                do_slimit(input_file, output, self.mangle)
        finally:
            if ('combined_filename' in locals() and
                os.path.exists(combined_filename)):
                os.remove(combined_filename)

    def run(self):
        """runner"""
        def output_path(source):
            "Set output path"
            name = os.path.splitext(os.path.basename(source))[0]
            return self.output % name
        
        if not self.sources:
            return
        
        if '%' in self.output:
            sources_outputs = dict((source, output_path(source))
                                   for source in self.sources)
        
            outputs = set(sources_outputs.values())
            sources_outputs = dict((src, out)
                                   for (src, out) in sources_outputs.items()
                                   if src not in outputs)
        
            for source, output in sources_outputs.items():
                msg = '%s -> %s' % (source, output)
                self.execute(self._minify_operation,
                             ([source], output),
                             msg=msg)
        else:
            if self.output in self.sources:
                self.sources.remove(self.output)
        
            msg = '%s -> %s' % (' + '.join(self.sources), self.output)
            self.execute(self._minify_operation,
                         (self.sources, self.output),
                         msg=msg)

class tsantsa_css(TsantsaCmd):
    """Minify css using cssmin"""
    description = """Minify CSS resources"""
    minification_type = 'css'


class tsantsa_js(TsantsaCmd):
    """Minify js using slimit"""
    description = """Minify JavaScript resources"""

    user_options = TsantsaCmd.user_options + [
        ('mangle', None, 'mangle names'),
    ]

    def initialize_options(self):
        TsantsaCmd.initialize_options(self)
        self.mangle = False
