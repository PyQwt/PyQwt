"""pyqt_distutils.command.build_ext

Implements the PyQtDistutils 'build_ext' command.
"""
# Copyright (C) 2003 Gerard Vermeulen
#
# This file is part of PyQwt
#
# PyQwt is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PyQwt is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU  General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, Gerard Vermeulen gives permission to
# link PyQwt with commercial, non-commercial and educational versions of Qt,
# PyQt and sip, and distribute PyQwt in this form, provided that equally
# powerful versions of Qt, PyQt and sip have been released under the terms
# of the GNU General Public License.
#
# If PyQwt is linked with commercial, non-commercial and educational versions
# of Qt, PyQt and sip, Python scripts using PyQwt do not have to be released
# under the terms of the GNU General Public License. 
#
# You must obey the GNU General Public License in all respects for all of the
# code used other than Qt, PyQt and sip, including the Python scripts that are
# part of PyQwt.


from distutils.command.build_ext import build_ext as old_build_ext
from distutils.ccompiler import new_compiler
from pyqt_distutils.configure import get_config
from pyqt_distutils.sysconfig import customize_qt_compiler

class build_ext(old_build_ext):

    def build_extensions(self):

        # First, sanity-check the 'extensions' list
        self.check_extensions_list(self.extensions)

        self.qt_compiler = new_compiler(verbose=self.verbose,
                                         dry_run=self.dry_run,
                                         force=self.force)
        
        customize_qt_compiler(self.qt_compiler,
                              get_config('qt').get('make'),
                              get_config('qt').get('type'))

        for ext in self.extensions:
            if 'qt' in ext.config_jobs:
                self.build_pyqt_extension(ext)
            else:
                self.build_extension(ext)

    # build_extensions()

    def build_pyqt_extension(self, ext):

        self.configure(ext)

        self.announce('Switching to the compiler for Qt extensions.')
        self.compiler, self.qt_compiler = self.qt_compiler, self.compiler
        old_build_ext.build_extension(self, ext)
        self.announce('Switching to the compiler for vanilla extensions.')
        self.compiler, self.qt_compiler = self.qt_compiler, self.compiler
        # FIXME: only for Windows
        # copy lib*.exp and lib*.lib from temp* to lib* directory (switch)

    # build_pyqt_extension()

    def configure(self, ext):
        for config_job in ext.config_jobs:
            info = get_config(config_job)
            for key in [
                'include_dirs',
                'define_macros',
                'undef_macros',
                'library_dirs',
                'libraries',
                'runtime_library_dirs',
                'extra_objects',
                'extra_compile_args',
                'extra_link_args',
                'export_symbols',
                ]:
                for item in info.get(key, []):
                    if item not in getattr(ext, key):
                        getattr(ext, key).append(item)

    # configure()

# class build_ext

# Local Variables: ***
# mode: python ***
# End: ***
