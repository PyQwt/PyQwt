""" pyqt_distutils/sysconfig.py

Provides customize_qt_compiler.
"""
#
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
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, Gerard Vermeulen gives permission to
# link PyQwt dynamically with commercial, non-commercial or educational
# versions of Qt, PyQt and sip, and distribute PyQwt in this form, provided
# that equally powerful versions of Qt, PyQt and sip have been released under
# the terms of the GNU General Public License.
#
# If PyQwt is dynamically linked with commercial, non-commercial or educational
# versions of Qt, PyQt and sip, PyQwt becomes a free plug-in for a non-free
# program.


from distutils.sysconfig import get_config_vars, get_python_inc

def customize_qt_compiler(compiler, make_info, type, ccache=None):
    """Customize the compiler for extension modules using Qt.
    """

    if compiler.compiler_type == "unix":
        if 'thread' in type:
            preprocessor = (
                '%(CXX)s -E '
                '%(CXXFLAGS_THREAD)s '
                ) % make_info
            compiler_so = (
                '%(CXX)s '
                '%(CXXFLAGS)s '
                '%(CXXFLAGS_THREAD)s '
                '%(CXXFLAGS_RELEASE)s '
                '%(CXXFLAGS_SHLIB)s '
                '%(CXXFLAGS_WARN_ON)s '
                ) % make_info
        else:
            preprocessor = (
                '%(CXX)s -E '
                ) % make_info
            compiler_so = (
                '%(CXX)s '
                '%(CXXFLAGS)s '
                '%(CXXFLAGS_RELEASE)s '
                '%(CXXFLAGS_SHLIB)s '
                '%(CXXFLAGS_WARN_ON)s '
                ) % make_info

        linker_so = (
            '%(CXX)s '
##             '%(RPATH)s%(LIBDIR_QT)s '
            '%(LFLAGS_PLUGIN)s '
            ) % make_info

        # Flag Python-2.3 to use a C++-linker, do not use ccache. 
        compiler_cxx = (
            '%(CXX)s'
            ) % make_info
        
        if ccache and -1 == preprocessor.find('ccache'):
            preprocessor = '%s %s' % (ccache, preprocessor)

        if ccache and -1 == compiler_so.find('ccache'):
            compiler_so = '%s %s' % (ccache, compiler_so)

        if  hasattr(compiler, 'compiler_cxx'):
            # Python-2.3.x
            compiler.set_executables(preprocessor=preprocessor,
                                     compiler_so=compiler_so,
                                     linker_so=linker_so,
                                     compiler_cxx=compiler_cxx)
        else:
            # Python-2.2.x, Python-2.1.x, Python-2.0.x
            compiler.set_executables(preprocessor=preprocessor,
                                     compiler_so=compiler_so,
                                     linker_so=linker_so)

        compiler.shared_lib_extension = get_config_vars('SO')

    if compiler.compiler_type == "msvc":
        compile_options = (
            '%(CXXFLAGS)s '
            '%(CXXFLAGS_RELEASE)s '
            '%(CXXFLAGS_MT_DLL)s '
            '%(CXXFLAGS_WARN_ON)s '
            ) % make_info
        compiler.compile_options = compile_options.split()
        ldflags_shared = (
            '%(LFLAGS)s '
            '%(LFLAGS_WINDOWS_DLL)s '
            ) % make_info
        compiler.ldflags_shared = ldflags_shared.split()

# customize_qt_compiler()

# Local Variables: ***
# mode: python ***
# End: ***
