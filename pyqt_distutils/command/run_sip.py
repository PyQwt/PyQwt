"""distutils.command.run_sip

Implements the PyQtDistutils 'run_sip' command.
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


import copy, glob, os, shutil
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
        ('sip-t-tags=', None,
         "enable this list of timeline and platform tags"),
        ('sip-x-features=', None,
         "disable this list of features"),
        ]

    boolean_options = ['concatenate', 'force']

    def initialize_options(self):
        self.extensions = None
        self.build_temp = None
        self.concatenate = 0
        self.force = None
        self.sip_program = None
        self.sip_file_dirs = None
        self.sip_t_tags = None
        self.sip_x_features = None

    # initialize_options()
    
    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_temp', 'build_temp'),
                                   ('force', 'force'))

        self.extensions = self.distribution.ext_modules
        
        if not self.sip_program:
            self.sip_program = get_config('sip').get('sip_program')
        assert self.sip_program

        self.sip_version = get_config('sip').get('sip_version')
        assert self.sip_version

        self.sip_file_dirs = self.sip_file_dirs or []
        if self.sip_file_dirs:
            self.sip_file_dirs = self.sip_file_dirs.split(os.pathsep)

        self.ensure_string_list('sip_t_tags')
        self.sip_t_tags = self.sip_t_tags or []

        self.ensure_string_list('sip_x_features')
        self.sip_x_features = self.sip_x_features or []

    # finalize_options()

    def __flag_list(self, flag, list):
        result = []
        for item in list:
            result.extend([flag, item])
        return result

    # __flag_list()

    def __run_sip(self, ext, sip_temp):
        """Run sip.
        """

        # clean
        if os.path.isdir(sip_temp):
            shutil.rmtree(sip_temp, 1)
        self.mkpath(sip_temp)

        # prepare and run sip
        sip_file_dirs = copy.copy(self.sip_file_dirs)
        sip_t_tags = copy.copy(self.sip_t_tags)
        sip_x_features = copy.copy(self.sip_x_features)
        for config in ext.config_jobs:
            for file_dir in get_config(config).get('sip_file_dirs', []):
                if file_dir not in sip_file_dirs:
                    sip_file_dirs.append(file_dir)
            for t_tag in get_config(config).get('sip_t_tags', []):
                if t_tag not in sip_t_tags:
                    sip_t_tags.append(t_tag)
            for x_feature in get_config(config).get('sip_x_features', []):
                if x_feature not in sip_x_features:
                    sip_x_features.append(x_feature)
        # replace '\\' with '/' because MSVC chokes on Windows path separators.
        sip_file_dirs = [item.replace('\\', '/') for item in sip_file_dirs] 
        cmd = (
            [self.sip_program]
            + self.__flag_list('-t', sip_t_tags)
            + self.__flag_list('-x', sip_x_features)
            + ['-c', sip_temp]
            + self.__flag_list('-I', sip_file_dirs)
            + [ext.sip_module]
            )
        self.spawn(cmd)
        # apply an eventual patch
        ext.sip_post_hook(sip_temp, ext.tag)
        if self.sip_version < 0x040000:
            # copy the wrapper
            self.copy_file(os.path.join(sip_temp, '%s.py' % ext.tag),
                           os.path.join(ext.path, '%s.py' % ext.tag))

    # __run_sip()
    
    def run(self):
        """Run sip, trying to minimize costly recompilation.

        - direct sip output to a temporary directory.
        - do a lazy copy of the *.{cpp,h} files to the package directory.
        - add the *.cpp files produced by sip to the source file list.
        - check if sip produced input for moc and act accordingly.
        """
        
        if not self.distribution.has_sip_sources():
            return
        for ext in [item for item in self.extensions if item.sip_module]:
            # setup
            sip_temp = os.path.join(self.build_temp, 'sip', ext.path)
            if self.sip_version < 0x040000:
                target = os.path.join(sip_temp, '%scmodule.cpp' % ext.tag)
            else:
                target = os.path.join(sip_temp, 'sip%scmodule.cpp' % ext.tag)
                
            # __run_sip
            if (self.force or newer_group(ext.sip_sources, target)):
                exec_msg = "generate the sources from '%s'" % ext.sip_module
                self.execute(self.__run_sip, (ext, sip_temp), exec_msg)

            # handle the *.cpp files generated by sip
            sources = (
                glob.glob(os.path.join(sip_temp, '%s*.cpp' % ext.tag)) # sip-3
                + glob.glob(os.path.join(sip_temp, 'sip%s*.cpp' % ext.tag)))

            # concatenate
            if self.concatenate:
                name = os.path.join(sip_temp, '%shuge.cpp' % ext.tag)
                print "concatenate the *.cpp files into '%s'" % name
                file = open(name, 'w')
                for source in sources:
                    file.write(open(source).read())
                file.close()
                sources = [name]

            # lazy copy and add *.cpp sources
            source_copies = 0
            for source in sources:
                target = os.path.join(ext.path, os.path.basename(source))
                if self.lazy_copy_sip_output_file(source, target):
                    source_copies += 1
                if target not in ext.sources:
                    ext.sources.append(target)

            # lazy copy the *.h sources
            headers = glob.glob(os.path.join(sip_temp, '*.h'))
            header_copies = 0
            for header in headers:
                target = os.path.join(ext.path, os.path.basename(header))
                if self.lazy_copy_sip_output_file(header, target):
                    header_copies += 1
                    
            print 'lazy copy %s .cpp and %s .h files' \
                  % (source_copies, header_copies)

            # add moc input generated by sip
            if self.sip_version < 0x040000:
                sip_proxy = os.path.join(ext.path, '%scmodule.h' % ext.tag)
            else:
                sip_proxy = os.path.join(ext.path, 'sip%scmodule.h' % ext.tag)
            if (os.path.exists(sip_proxy)
                and not sip_proxy in ext.moc_sources):
                ext.moc_sources.append(sip_proxy)
    # run()

    def lazy_copy_sip_output_file(self, source, target):
        """Lazy copy a sip output file to another sip output file.
        
        - check if source and target sip do really differ.
        - copy the source file to the target if they do.
        - return True if on copy and False on no copy.
        """
        if not os.path.exists(target) or self.force:
            self.copy_file(source, target)
            return True

        file = open(source)
        sourcelines = file.readlines()
        file.close()
        file = open(target)
        targetlines = file.readlines()
        file.close()
    
        # global length check
        if len(sourcelines) != len(targetlines):
            self.copy_file(source, target)
            return True

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
                return True
            line = line + 1

        return False
        
    # lazy_copy_sip_output_file()

# class run_sip

# Local Variables: ***
# mode: python ***
# End: ***
