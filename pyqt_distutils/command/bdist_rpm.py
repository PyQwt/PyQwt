"""pyqt_distutils.command.build

Implements the PyQtDistutils 'bdist' command.

Overridden to support PyQt and sip.
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


from distutils.command.bdist_rpm import bdist_rpm as old_bdist_rpm
from pyqt_distutils.configure import get_config

class bdist_rpm(old_bdist_rpm):
    
    def run(self):
        tag = '_Qt%s%s%s' % tuple(
            get_config('qt').get('qt_version_str').split('.'))
        name = self.distribution.metadata.name
        if -1 == name.find(tag):
            self.distribution.metadata.name = name + tag
        old_bdist_rpm.run(self)

    # run()

# class bdist_rpm

# Local Variables: ***
# mode: python ***
# End: ***
    
