""" pyqt_distutils/sysconfig.py

Provides customize_qt_compiler.
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


from distutils.sysconfig import get_config_vars, get_python_inc

def customize_qt_compiler(compiler, make_info, type):
    """Customize the compiler for extension modules using Qt.
    """
    compiler.macros.append(('NDEBUG', None))
    compiler.macros.append(('QT_NODEBUG', None))

    compiler.include_dirs.append(make_info['INCDIR_QT'])
    compiler.include_dirs.append(get_python_inc())

    compiler.library_dirs.append(make_info['LIBDIR_QT'])

    if compiler.compiler_type == "unix":
        llibraries = [] # libraries are prefixed by '-l'
        if 'thread' in type:
            llibraries.append(make_info['LIBS_QT_THREAD'])
            llibraries.append(make_info['LIBS_THREAD'])
            compiler.macros.append(('QT_THREAD_SUPPORT', None))
            preprocessor = (
                '%(CXX)s -E '
                '%(CXXFLAGS_THREAD)s '
                ) % make_info
            compiler_so = (
                '%(CXX)s '
                '%(CXXFLAGS_THREAD)s '
                '%(CXXFLAGS_RELEASE)s '
                '%(CXXFLAGS_SHLIB)s '
                '%(CXXFLAGS_WARN_ON)s '
                ) % make_info
            linker_so = (
                '%(CXX)s '
                '%(LFLAGS_PLUGIN)s '
                ) % make_info
        else:
            compiler.libraries.append(make_info['LIBS_QT'])
            preprocessor = (
                '%(CXX)s -E '
                ) % make_info
            compiler_so = (
                '%(CXX)s '
                '%(CXXFLAGS_RELEASE)s '
                '%(CXXFLAGS_SHLIB)s '
                '%(CXXFLAGS_WARN_ON)s '
                ) % make_info
            linker_so = (
                '%(CXX)s '
                '%(LFLAGS_PLUGIN)s '
                ) % make_info
        
        compiler.set_executables(preprocessor=preprocessor,
                                 compiler_so=compiler_so,
                                 linker_so=linker_so)
        compiler.shared_lib_extension = get_config_vars('SO')
        llibraries = ' '.join(llibraries).split()
        for llibrary in llibraries:
            library = llibrary[2:]
            if not library in compiler.libraries:
                compiler.libraries.append(library)

    if compiler.compiler_type == "msvc":
        compiler.macros.append(('QT_DLL', None))
        compiler.macros.append(('QT_THREAD_SUPPORT', None))
        compiler.libraries.append(make_info['LIBS_QT_THREAD'])
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
##         compiler.compile_options = [
##             '-nologo', '-O1', '-MD', '-W3',
##             ]
##         compiler.compile_options_debug = [
##             '-nologo', '-Zi', '-MDd', '-W3', '-U_DEBUG',
##             ]
##         compiler.ldflags_shared = [
##             '/NOLOGO', '/SUBSYSTEM:windows', '/DLL',
##             ]
##         compiler.ldflags_shared_debug = [
##             '/NOLOGO', '/DEBUG', '/SUBSYSTEM:windows', '/DLL',
##             ]

# customize_qt_compiler()
