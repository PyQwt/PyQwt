"""distutils.command.run_sip

Implements the PyQtDistutils 'run_sip' command.
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
# FOR A PARTICULAR PURPOSE.  See the GNU  General Public License for more
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


import glob
import os
import shutil
from distutils.core import Command
from distutils.dep_util import newer_group 
from pyqt_distutils.configure import get_config

            
class run_sip(Command):

    description = "Run sip (PyQt's Simple Interface Program)."

    user_options = [
        ('build-temp', 't',
         "directory to put temporary build by-products"),
        ('concatenate', 'c',
         "concatenate the C++ source files made by sip"),
        ('force', 'f',
         "forcibly build everything (ignore file timestamps)"),
        ('sip-program=', 's',
         "specify sip (Simple Interface Program)"),
        ('sip-file-dirs=', 'I',
         "list of directories to search for *.sip files (separated by '%s')"
         % os.pathsep),
        ('sip-t-options=', None,
         "target code for this timeline and platform pair (separated by ',')"),
        ('sip-x-features=', None,
         "disable this list of features (separated by ',')"),
        ]

    boolean_options = ['concatenate', 'force']

    def initialize_options(self):
        self.build_temp = None
        self.concatenate = 0
        self.force = None
        self.sip_program = None
        self.sip_file_dirs = None
        self.sip_t_options = None
        self.sip_x_features = None

    # initialize_options()
    
    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_temp', 'build_temp'),
                                   ('force', 'force'))

        if not self.sip_program: 
            self.sip_program = get_config('sip').get('sip_program')

        self.sip_file_dirs = self.sip_file_dirs or []
        if self.sip_file_dirs:
            self.sip_file_dirs = self.sip_file_dirs.split(os.pathsep)

        self.sip_t_options = self.sip_t_options or []
        if self.sip_t_options:
            self.sip_t_options = self.sip_t_options.split(',')
        else:
            self.sip_t_options = get_config('qt').get('sip_t_options')

        self.sip_x_features = self.sip_x_features or []
        if self.sip_x_features:
            self.sip_x_features = self.sip_x_features.split(',')
        self.sip_x_features.extend(get_config('sip').get('sip_x_features'))

        assert self.sip_program

    # finalize_options()

    def __flag_list(self, flag, list):
        result = []
        for item in list:
            result.extend([flag, item])
        return result

    # __flag_list()
    
    def __run_sip(self, ext, sip_temp):
        """Run sip, trying to minimize costly recompilation.

        Algorithm:
        - Direct sip output to a temporary directory.
        - Call post_sip_hook to patch the sip output, if needed.
        - Copy the Python wrapper to the package directory.
        - Do a 'smart' copy of the *.{cpp,h} files to the package directory.
        - Add the *.cpp files produced by sip to the source file list.
        - Check if sip produced input for moc and act accordingly.
        """

        # ext.who means "package directory" and "sip module name"
        # clean
        if os.path.isdir(sip_temp):
            shutil.rmtree(sip_temp, 1)
        self.mkpath(sip_temp)
        # replace '\\' with '/' because MSVC chokes on Windows path separators.
        sip_file_dirs = []
        for sip_file_dir in ext.sip_file_dirs + self.sip_file_dirs:
            sip_file_dirs.append(sip_file_dir.replace('\\', '/'))
        sip_module = ext.sip_module.replace('\\', '/')
        # prepare and run sip
        cmd = (
            [self.sip_program]
            + self.__flag_list('-t', self.sip_t_options)
            + self.__flag_list('-x', self.sip_x_features)
            + ['-c', sip_temp]
            + self.__flag_list('-I', sip_file_dirs)
            + [sip_module]
            )
        self.spawn(cmd)
        # apply an eventual patch
        ext.sip_post_hook(sip_temp, ext.who)
        # copy the wrapper
        self.mkpath(os.path.dirname(ext.pkg_wrapper))
        self.copy_file(
            os.path.join(sip_temp, '%s.py' % ext.who), ext.pkg_wrapper)

    # __run_sip()
    
    def run(self):
        if not self.distribution.has_sip_sources():
            return
        for ext in [m for m in self.distribution.ext_modules if m.sip_module]:
            # run_sip
            sip_temp = os.path.join(self.build_temp, 'sip_%s' % ext.who)
            if (self.force or newer_group(ext.sip_sources, ext.pkg_wrapper)):
                exec_msg = "generate the sources from '%s'" % ext.sip_module
                self.execute(self.__run_sip, (ext, sip_temp), exec_msg)

            # handle the *.cpp files generated by sip
            sources = glob.glob(
                os.path.join(sip_temp, '%scmodule.cpp' % ext.who))
            sources += glob.glob(
                os.path.join(sip_temp, 'sip%s*.cpp' % ext.who))

            # concatenate
            if self.concatenate:
                name = os.path.join(sip_temp, '%shuge.cpp' % ext.who)
                self.announce("concatenate the *.cpp files into '%s'" % name)
                file = open(name, 'w')
                for source in sources:
                    file.write(open(source).read())
                file.close()
                sources = [name]

            # lazy copy and add *.cpp sources
            for source in sources:
                target = os.path.join(ext.who, os.path.basename(source))
                self.__lazy_copy_sip_output_file(source, target)
                if target not in ext.sources:
                    ext.sources.append(target)

            # lazy copy the *.h sources
            for source in glob.glob(os.path.join(sip_temp, '*.h')):
                target = os.path.join(ext.who, os.path.basename(source))
                self.__lazy_copy_sip_output_file(source, target)

            # add eventual moc input generated by sip
            sip_proxy = os.path.join(
                ext.who, 'sip%sProxy%s.h' % (ext.who, ext.who)) 
            if (os.path.exists(sip_proxy)
                and not sip_proxy in ext.moc_sources):
                ext.moc_sources.append(sip_proxy)

    # run()

    def __lazy_copy_sip_output_file(self, source, target):
        """Checks if two files generated by sip do really differ.
        """
        if not os.path.exists(target) or self.force:
            self.copy_file(source, target)
            return

        file = open(source)
        sourcelines = file.readlines()
        file.close()
        file = open(target)
        targetlines = file.readlines()
        file.close()
    
        # global length check
        if len(sourcelines) != len(targetlines):
            self.copy_file(source, target)
            return

        # skip header comments by looking for the first '#define'
        line = 0
        while line < len(sourcelines):
            if sourcelines[line][0] == "#":
                break
            line = line + 1

        # line by line check
        while line < len(sourcelines):
            if sourcelines[line] != targetlines[line]:
                self.copy_file(source, target)
                return
            line = line + 1
        
    # lazy_copy_sip_output_files()

# class run_sip

# Local Variables: ***
# mode: python ***
# End: ***
