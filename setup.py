#!/usr/bin/env python

import os, time
from distutils.core import setup

print '***** BIG FAT WARNING *****'
print 'Use configure.py to build and install PyQwt:'
print '  cd configure'
print '  python configure.py --help'  
print 'The setup.py script serves only to make a source distribution.'
print

name = 'PyQwt'
snapshot = '%04d%02d%02d' % (time.localtime()[:3])
version = '4.2'
long_description = """
PyQwt is a set of Python bindings for the Qwt C++ class library.
The Qwt library extends the Qt framework with widgets for
Scientific and Engineering applications.   It provides a widget
to plot data points in two dimensions and various widgets to
display and control bounded or unbounded floating point values.

PyQwt requires and extends PyQt, a set of Python bindings for Qt.

It is highly recommended to use PyQwt with either Numeric,
numarray or both.  Numeric and/or numarray extend the Python
language with new data types that make Python an ideal language
for numerical computing and experimentation like MatLab and IDL.
                                                                
Copyright (C) 2001-2005 Gerard Vermeulen
Copyright (C) 2000 Mark Colclough

PyQwt is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

PyQwt is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyQwt; if not, write to the Free Software Foundation,
Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

In addition, as a special exception, Gerard Vermeulen gives
permission to link PyQwt dynamically with commercial, non-commercial
or educational versions of Qt, PyQt and sip, and distribute PyQwt
in this form, provided that equally powerful versions of Qt, PyQt
and sip have been released under the terms of the GNU General
Public License.

If PyQwt is dynamically linked with commercial, non-commercial or
educational versions of Qt, PyQt and sip, PyQwt becomes a free
plug-in for a non-free program.
"""

setup(
    name              = name,
    version           = version,
    description       = "Python bindings for the Qwt library",
    url               = "http://pyqwt.sourceforge.net",
    author            = "Gerard Vermeulen",
    author_email      = "gerard.vermeulen@grenoble.cnrs.fr",
    license           = "GPL",
    long_description  = long_description,
    platforms         = "Unix, Windows (MSVC), MacOS/X",
    )

# Local Variables: ***
# compile-command: "python setup.py sdist" ***
# End: ***
