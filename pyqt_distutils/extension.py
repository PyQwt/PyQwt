"""pyqt_distutils.extension

Provides the Extension class, used to describe C/C++ extension
modules in setup scripts.

Hacked to support PyQt and sip.
"""
#
# Copyright (C) 2003-2004 Gerard Vermeulen
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


import os
from glob import glob
from os.path import join
from pyqt_distutils.configure import get_config
from distutils.core import Extension as OldExtension
from distutils.errors import DistutilsInternalError, DistutilsFileError 


class Extension(OldExtension):
    """Describes an extension module with support for PyQt and sip.

    New attributes with respect to (Old)Extension are:
    - sip_module : string
    - sip_file_dirs : [strings]
    - post_sip_hook: callable(directory, name)
    - moc_sources : [strings]
    - config_jobs : [strings]
    """

    def __init__(
        self,
        name,
        sources,
        ## the new sip and moc related stuff
        sip_module=None,
        sip_file_dirs=None,
        sip_post_hook=None,
        moc_sources=None,
        config_jobs=None,
        ## old stuff
        include_dirs=None,
        define_macros=None,
        undef_macros=None,
        library_dirs=None,
        libraries=None,
        runtime_library_dirs=None,
        extra_objects=None,
        extra_compile_args=None,
        extra_link_args=None,
        export_symbols=None,
        ):

        OldExtension.__init__(
            self,
            name,
            sources,
            include_dirs,
            define_macros,
            undef_macros,
            library_dirs,
            libraries,
            runtime_library_dirs,
            extra_objects,
            extra_compile_args,
            extra_link_args,
            export_symbols
            )

        self.sip_module = sip_module or ''
        self.sip_file_dirs = sip_file_dirs or []
        self.sip_post_hook = sip_post_hook or (lambda directory, name: None)
        self.moc_sources = moc_sources or []
        self.config_jobs = config_jobs or []

        if self.sip_module:
            self.sip_sources = [self.sip_module]
            sip_file_dir = os.path.dirname(self.sip_module)
            if sip_file_dir and not sip_file_dir in self.sip_file_dirs:
                self.sip_file_dirs.insert(0, sip_file_dir)
            # hack to make the old style sip modules work as libraries on Posix
            if get_config('sip').get('sip_version') < 0x040000:
                make_info = get_config('qt').get('make')
                lflags_soname = make_info.get('LFLAGS_SONAME')
                if lflags_soname:
                    extension_shlib = make_info.get('EXTENSION_SHLIB', '.so')
                    self.extra_link_args.append(lflags_soname
                                                + self.name.split('.')[-1]
                                                + extension_shlib)
        else:
            self.sip_sources = []
            
        # + check if all hand written C/C++ sources exist
        for source in self.sources:
            if not os.path.exists(source):
                raise DistutilsFileError, (
                    "<sources> contains a missing file '%s'." % source
                    )

        # + check if all header files to be processed by moc exist
        for source in self.moc_sources:
            if not os.path.exists(source):
                raise DistutilsFileError, (
                    "<moc_sources> contains a missing file '%s'." % source
                    )

        # pyqt_distutils.core.setup plugs "package info" into Distribution 
        self.path = self.name.split('.')
        assert len(self.path) >= 2 # FIXME: accept only *real* packages
        package = '.'.join(self.path[0:-1])
        self.path = apply(os.path.join, self.path[0:-1])
        self.packages = [package]
        self.package_dir = {package: package}

        # parse information from the sip module file
        # + find the sip module name
        # + find all sip sources: the sip module and files included by it
        self.tag = ''
        if self.sip_module:
            self.tag = get_sip_module_tag(self.sip_module)
            self.sip_sources = get_sip_includes(
                self.sip_module, self.sip_sources)
           
    # __init__()

# class Extension


def get_sip_module_tag(sip_file):
    for line in file(sip_file, 'r').readlines():
        if line[:7] == '%Module':
            return line.split()[1]

# get_sip_module_name()


def get_sip_includes(sip_file, includes=[]):
    directory = os.path.dirname(sip_file)
    for line in file(sip_file, 'r').readlines():
        if line[:8] == '%Include':
            include = os.path.join(directory, line[8:].strip())
            if os.path.exists(include):
                if not include in includes:
                    includes.append(include)
            else:
                raise DistutilsFileError, (
                    "'%s' includes a missing file '%s'." % (sip_file, include)
                    )
    return includes

# get_sip_includes()


# Local Variables: ***
# mode: python ***
# End: ***
