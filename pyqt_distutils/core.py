"""pyqt_distutils.core

The only module that needs to be imported to use the PyQtDistutils; provides
the 'setup' function (which is to be called from the setup script).  Also
indirectly provides the Distribution and Command classes, although they are
really defined in pyqt_distutils.dist and pyqt_distutils.cmd.

Hacked to support PyQt and sip.
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


from distutils.core import *
from distutils.core import setup as old_setup

from pyqt_distutils.extension import Extension
from pyqt_distutils.dist import Distribution

from pyqt_distutils.command import build
from pyqt_distutils.command import build_ext
from pyqt_distutils.command import run_sip
from pyqt_distutils.command import run_moc
from pyqt_distutils.command import bdist
from pyqt_distutils.command import bdist_dumb
from pyqt_distutils.command import bdist_rpm
from pyqt_distutils.command import bdist_wininst

def setup(**attr):
    distclass = Distribution
    cmdclass = {
        'build': build.build,
        'build_ext': build_ext.build_ext,
        'run_sip': run_sip.run_sip,
        'run_moc': run_moc.run_moc,
        'bdist': bdist.bdist,
        'bdist_dumb': bdist_dumb.bdist_dumb,
        'bdist_rpm': bdist_rpm.bdist_rpm,
        'bdist_wininst': bdist_wininst.bdist_wininst,
        }

    new_attr = attr.copy()

    if new_attr.has_key('cmdclass'):
        cmdclass.update(new_attr['cmdclass'])
    new_attr['cmdclass'] = cmdclass

    if not new_attr.has_key('distclass'):
        new_attr['distclass'] = distclass

    # Hack package info for the sip generated extension module wrappers.
    if not new_attr.has_key('packages'):
        new_attr['packages'] = []
    if not new_attr.has_key('package_dir'):
        new_attr['package_dir'] = {}
    if new_attr.has_key('ext_modules'):
        for ext in new_attr['ext_modules']:
            new_attr['packages'].extend(ext.packages)
            for package, directory in ext.package_dir.items():
                new_attr['package_dir'][package] = directory

    #print 'packages:', new_attr['packages']
    #print 'package_dir:', new_attr['package_dir']
    
    return old_setup(**new_attr)

# setup() 

# Local Variables: ***
# mode: python ***
# End: ***
