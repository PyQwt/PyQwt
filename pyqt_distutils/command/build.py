"""pyqt_distutils.command.build

Implements the PyQtDistutils 'build' command.

Overridden to support PyQt and sip.
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


from distutils.command.build import build as old_build

class build(old_build):
    
    def has_moc_sources(self):
        return self.distribution.has_moc_sources()

    # has_moc_sources()
    
    def has_sip_sources(self):
        return self.distribution.has_sip_sources()

    # has_sip_sources()

    sub_commands = [
        ('run_sip',       has_sip_sources),
        ('run_moc',       has_moc_sources),
        ('build_py',      old_build.has_pure_modules),
        ('build_clib',    old_build.has_c_libraries),
        ('build_ext',     old_build.has_ext_modules),
        ('build_scripts', old_build.has_scripts),
        ]

# class build

# Local Variables: ***
# mode: python ***
# End: ***
    
