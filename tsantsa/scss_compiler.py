# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Andrew Colin Kissa <andrew@topdog.za.net>.
# Based on minify Copyright (c) 2011-2012 Sylvain Prat
# This program is open-source software, and may be redistributed
# under the terms of the MIT license. See the LICENSE file in this
# distribution for details
"""
Tsantsa - SCSS compliation plugin for setup tools
"""

import os

import scss

from tsantsa import TsantsaBaseCmd, remove_duplicates


class ScssCompileCmd(TsantsaBaseCmd):
    """tsantsa scss compile setuptools command"""

    user_options = [
        ('sources=', None, 'sources files'),
        ('output=', None, 'compiled css output file'),
        ('loadpaths=', None, 'paths pyScss will look ".scss" files in '
                             'This can be the path to the compass '
                             'framework or blueprint or compass-recepies'
                             ', etc'),
    ]

    def initialize_options(self):
        """init options"""
        TsantsaBaseCmd.initialize_options(self)
        self.loadpaths = []

    def finalize_options(self):
        """finalize options"""
        clean_path = os.path.normcase
        default_output = '%s.css'
        self.ensure_string('output', default_output)
        self.output = clean_path(self.output)
        self.ensure_string_list('sources')
        if self.sources:
            self.sources = remove_duplicates(clean_path(path)
                            for path in self._files_list(self.sources))
        self.ensure_string_list('loadpaths')
        if self.loadpaths:
            self.loadpaths = remove_duplicates(clean_path(path)
                            for path in self._files_list(self.loadpaths)
                            if os.path.isdir(clean_path(path)) and
                            not clean_path(path) is None )

    def _compile(self, sources, output):
        """Run a compilation operation on the sources"""
        try:
            input_file = sources.pop()
            if len(sources) > 1:
                combined_filename = self._create_temporary_file()
                self._combine_files(sources, combined_filename)
                input_file = combined_filename

            scss.LOAD_PATHS = self.loadpaths
            parser = scss.Scss(scss_opts = {'compress_reverse_colors': False})
            with open(output, mode='wb') as out:
                out.write(parser.compile(open(input_file, mode='rb').read()))
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
                self.execute(self._compile,
                             ([source], output),
                             msg=msg)
        else:
            if self.output in self.sources:
                self.sources.remove(self.output)
        
            msg = '%s -> %s' % (' + '.join(self.sources), self.output)
            self.execute(self._compile,
                         (self.sources, self.output),
                         msg=msg)


class compile_scss(ScssCompileCmd):
    """Compile SCSS using pyScss"""
    description = """Compile SCSS to css"""

