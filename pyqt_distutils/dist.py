"""pyqt_distutils.dist

Provides the Distribution class, which represents the module distribution
being built/installed/distributed.

Hacked to support PyQt and sip.
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


from distutils.dist import *
from distutils.dist import Distribution as OldDistribution

class Distribution(OldDistribution):
    """The core of the PyQtDistutils.
    """

    def __init__(self, attrs=None):
        OldDistribution.__init__(self, attrs)

    # __init__()
    
    def has_sip_sources(self):
        if self.has_ext_modules():
            for ext in self.ext_modules:
                if len(ext.sip_sources):
                    return 1
        return 0

    # has_sip_sources()
                
    def has_moc_sources(self):
        if self.has_ext_modules():
            for ext in self.ext_modules:
                if len(ext.moc_sources) + len(ext.sip_sources):
                    return 1
        return 0

    # has_moc_sources()

# class Distribution

# Local Variables: ***
# mode: python ***
# End: ***
