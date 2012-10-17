=======
Tsantsa
=======

Tsantsa provides setuptools commands for minifying CSS and JS resources and
compilation of SCSS resources to CSS using `cssmin`_, `slimit`_ and `scss`_.

scss, cssmin and slimit are pure Python packages and do not require any external commands.

This package is inspired by and based on the minify package by Sylvain Prat which uses the
`YUI compressor`_ from Yahoo! Inc.

When you install ``tsantsa``, three new commands are available:

- ``tsantsa_js`` which minifies Javascript files
- ``tsantsa_css`` which minifies CSS files
- ``compile_scss`` which compiles SCSS files to CSS

See the Usage_ section for more information about these commands.

.. _`YUI compressor`: http://developer.yahoo.com/yui/compressor/
.. _`cssmin`: https://github.com/zacharyvoase/cssmin
.. _`slimit`: http://slimit.org/
.. _`scss`: http://packages.python.org/scss/

Installation
============

The Tsantsa commands are meant to be used in an existing python project. So, in
order to make the commands available in your project, just add ``tsantsa`` to
the requirements of your project, for example::

    setup(
        ...
        install_requires=['tsantsa'],
        ...
    )

Then, when you install your package, the Tsantsa commands will be available.


Usage
=====

.. _Usage:


Tsantsa provides commands for minifying CSS and JS resources and compiling SCSS
resources:

- ``tsantsa_js`` which minifies Javascript files
- ``tsantsa_css`` which minifies CSS files
- ``compile_scss`` which compiles SCSS files to CSS


Minifying Javascript files
--------------------------

To show the options of the ``tsantsa_js`` command, just type::

    $ python setup.py tsantsa_js --help


You should obtain something like this::

    Common commands: (see '--help-commands' for more)
    
      setup.py build      will build the package underneath 'build/'
      setup.py install    will install the package
    
    Global options:
      --verbose (-v)  run verbosely (default)
      --quiet (-q)    run quietly (turns verbosity off)
      --dry-run (-n)  don't actually do anything
      --help (-h)     show detailed help message
      --no-user-cfg   ignore pydistutils.cfg in your home directory
    
    Options for 'tsantsa_js' command:
      --sources                sources files
      --output                 minified output filename. If you provide a template
                               output filename (e.g. "static/%s-min.ext"), the
                               source files will be minified individually
      --mangle                 mangle names
    
    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help

The ``tsantsa_js`` tool can be used on the command-line. Here is an example::

    $ python setup.py tsantsa_js --sources static/*.js --output static/combined.js


But, the most useful way to use ``tsantsa_js`` is via a ``setup.cfg`` file
located in your project root directory (that is, next to the ``setup.py``
file)::

    [tsantsa_js]
    sources = static/one.js static/two.js
    output = static/combined.js
    mangle = yes

Then, we you run the ``tsantsa_js`` command, the command options will be read
from the ``setup.cfg`` file in addition to the command-line arguments.

Note that, since there's a single output file for many sources, the
sources files are merged into a single file which is compressed to
produce a single minified file.

However, you may want to compress the sources files individually and obtain
distinct minified files. In that case, you should provide a template output
filename instead of a regular output filename. A template output filename is a
filename with a ``%s`` in it, which will be substituted by the current source
name being processed. For example::

    [tsantsa_js]
    sources = static/one.js static/two.js
    output = static/%s-min.js

Running ``python setup.py tsantsa_js`` will then produce two minified files:
``static/one-min.js`` and ``static/two-min.js``.


Minifying CSS files
-------------------

You can also see the options of the ``tsantsa_css`` command, by typing::

    $ python setup.py tsantsa_css --help

And here is the result::

    Common commands: (see '--help-commands' for more)
    
      setup.py build      will build the package underneath 'build/'
      setup.py install    will install the package
    
    Global options:
      --verbose (-v)  run verbosely (default)
      --quiet (-q)    run quietly (turns verbosity off)
      --dry-run (-n)  don't actually do anything
      --help (-h)     show detailed help message
      --no-user-cfg   ignore pydistutils.cfg in your home directory
    
    Options for 'tsantsa_css' command:
      --sources     sources files
      --output      minified output filename. If you provide a template output
                    filename (e.g. "static/%s-min.ext"), the source files will be
                    minified individually
    
    usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
       or: setup.py --help [cmd1 cmd2 ...]
       or: setup.py --help-commands
       or: setup.py cmd --help

This command can be used about the same way as the ``tsantsa_js`` command, but
it has less options.


Combining minification operations
---------------------------------

You can also combine minification operations thanks to the builtin ``alias``
command (still specified in the ``setup.cfg`` file, but not available with pure distutils)::

    [alias]
    minify_each_css = tsantsa_css --sources static/*.css --output static/%s-min.css
    minify_each_js = tsantsa_js --sources static/*.js --output static/%s-min.js
    minify_each = minify_each_css minify_each_js

Then call ``minify_each`` by typing:: 
    
    $ python setup.py minify_each


Compiling SCSS files
--------------------

You can also see the options of the ``compile_scss`` command, by typing::

    $ python setup.py compile_scss --help

And here is the result::

	Common commands: (see '--help-commands' for more)

	  setup.py build      will build the package underneath 'build/'
	  setup.py install    will install the package

	Global options:
	  --verbose (-v)  run verbosely (default)
	  --quiet (-q)    run quietly (turns verbosity off)
	  --dry-run (-n)  don't actually do anything
	  --help (-h)     show detailed help message
	  --no-user-cfg   ignore pydistutils.cfg in your home directory

	Options for 'compile_scss' command:
	  --sources  sources files
	  --output   compiled css output file

	usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
	   or: setup.py --help [cmd1 cmd2 ...]
	   or: setup.py --help-commands
	   or: setup.py cmd --help

Support
=======

This project is hosted on `Github
<https://github.com/akissa/tsantsa/>`__.
Please report issues via the bug tracker.