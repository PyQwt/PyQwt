#!/usr/bin/env python

import glob, os, sys, time

from distutils.errors import *
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

from pyqt_distutils.configure import get_config
from pyqt_distutils.core import setup
from pyqt_distutils.extension import Extension

#
# PLATFORM CHECK & SETUP.CFG INITIALIZATION
#
if os.name in ['nt', 'posix']:
    copy_file('setup_cfg_' + os.name, 'setup.cfg', update=1, verbose=0)
else:
    raise DistutilsPlatformError, "platform '%s' is unsupported." % os.name

#
# NAME & VERSION INFORMATION
#
name = 'PyQwt'
qwtdir = 'qwt-sources'
snapshot = '%04d%02d%02d' % (time.localtime()[:3])
version = '4.0'

#
# SIP VERSION
#
sip_version = get_config('sip').get('sip_version')
if sip_version and sip_version < 0x030900:
    raise SystemExit, ("Building '%s' with requires sip-3.9 or sip-4.0" % name)

#
# CHECK FOR A RECENT PYTHON
#
if sip_version < 0x040000:
    if (not hasattr(sys, 'version_info')
        or sys.version_info < (2,0,0, 'alpha', 0)
        or sys.version_info > (2,3,9, 'final', 0)):
        raise SystemExit, (
            "Building '%s' with sip-%s requires Python-2.3, 2.2, 2.1 or 2.0."
            % (sip_version, name))
else:
    if (not hasattr(sys, 'version_info')
        or sys.version_info < (2,3,0, 'alpha', 0)
        or sys.version_info > (2,3,9, 'final', 0)):
        raise SystemExit, (
            "Building '%s' with sip-%s requires Python-2.3."
            % (sip_version, name))
    

#
# EXTENSION MODULE INFO
#
sources = (glob.glob(os.path.join(qwtdir, 'src', '*.cpp')) +
           glob.glob(os.path.join('numpy', '*.cpp')))

moc_sources = [
    '%s/include/qwt_analog_clock.h' % qwtdir,
    '%s/include/qwt_compass.h' % qwtdir,
    '%s/include/qwt_counter.h' % qwtdir,
    '%s/include/qwt_dial.h' % qwtdir,
    '%s/include/qwt_dyngrid_layout.h' % qwtdir,
    '%s/include/qwt_knob.h' % qwtdir,
    '%s/include/qwt_legend.h' % qwtdir,
    '%s/include/qwt_picker.h' % qwtdir,
    '%s/include/qwt_plot.h' % qwtdir,
    '%s/include/qwt_plot_canvas.h' % qwtdir,
    '%s/include/qwt_plot_picker.h' % qwtdir,
    '%s/include/qwt_plot_zoomer.h' % qwtdir,
    '%s/include/qwt_push_button.h' % qwtdir,
    '%s/include/qwt_scale.h' % qwtdir,
    '%s/include/qwt_sldbase.h' % qwtdir,
    '%s/include/qwt_slider.h' % qwtdir,
    '%s/include/qwt_thermo.h' % qwtdir,
    '%s/include/qwt_wheel.h' % qwtdir,
    ]


if sip_version < 0x040000:
    dotted_name = 'qwt.lib_qwtc'
else:
    dotted_name = 'qwt._qwt'


pyqwt = Extension(
    dotted_name,
    sources,
    sip_module     = 'sip/qwtmod.sip',
    moc_sources    = moc_sources,
    config_jobs    = ['qt', 'sip', 'qt_module', 'numarray', 'numeric',],
    include_dirs   = ['qwt', 'numpy', '%s/include' % qwtdir],
    )

ext_modules = [pyqwt]

if os.name == 'posix':
    iqt = Extension(
        'iqt._iqt',
        ['iqt/_iqt.cpp'],
        config_jobs = ['qt'],
        )
    ext_modules.append(iqt)

#
# SETUP INFO
#


if os.name == 'nt':
    infix = name
elif os.name == 'posix':
    infix = ''

data_files = []

#
# documentation
#
data_files.append((os.path.join(infix, 'html'),
                   glob.glob(os.path.join('Doc', 'html', 'pyqwt', '*.css'))))
data_files.append((os.path.join(infix, 'html'),
                   glob.glob(os.path.join('Doc', 'html', 'pyqwt', '*.html'))))
data_files.append((os.path.join(infix, 'html'),
                   glob.glob(os.path.join('Doc', 'html', 'pyqwt', '*.png'))))
data_files.append((os.path.join(infix, 'html'),
                   glob.glob(os.path.join('Doc', 'html', 'pyqwt', '*.txt'))))
data_files.append((os.path.join(infix, 'html', 'qwt'),
                   glob.glob(os.path.join(qwtdir, 'doc', 'html', '*'))))

#
# examples
#
data_files.append((os.path.join(infix, 'examples'), ['examples/README']))
if os.name == 'nt':
    for filename in [
        'BodeDemo.py',
        'CPUplot.py',
        'CurveDemo1.py',
        'CurveDemo2.py',
        'CurveDemo3.py',
        'DataDemo.py',
        'DialDemo.py',
        'MapDemo.py',
        'MinPackDemo.py',
        'MultiDemo.py',
        'PyCute.py',
        'QwtImagePlotDemo.py',
        'RadioDemo.py',
        'SimpleDemo.py',
        'SliderDemo.py',
        'StackOrder.py',
        'histtool.py',
        ]:
        copy_file('examples/%s' % filename, 'examples/%sw' % filename)
    data_files.append((os.path.join(infix, 'examples'),
                       glob.glob('examples/*.pyw')))
elif os.name == 'posix':
    data_files.append((os.path.join(infix, 'examples'),
                       glob.glob('examples/*.py')))

#
# scripts
#
if os.name == 'nt':
    copy_file('examples/PyCute.py', 'examples/PyCute.pyw')
    scripts = ['examples/PyCute.pyw', 'examples/PyCute.bat']
elif os.name == 'posix':
    copy_file('examples/PyCute.py', 'examples/PyCute')
    scripts = ['examples/PyCute']

#
# description
#
long_description = """
PyQwt is FAST and EASY data plotting for Python, Numeric and Qt!
                                                                
The GNU General Public License applies to PyQwt with exceptions
for non-GPL'ed releases of Qt, PyQt and sip (see below).
"""

if os.name == 'nt':
    long_description = long_description + """
HTML documentation and example scripts can be found in
C:/Python*/PyQwt.

PyCute -- a Python shell for PyQt -- can be found in
C:/Python*/Scripts.
"""

long_description = long_description + """
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
"""

long_description = long_description + """
-----------------------------------------------------------------
                                                                
Copyright (C) 2001-2004 Gerard Vermeulen
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
    version           = snapshot,
    description       = "Python bindings for the Qwt library",
    url               = "http://pyqwt.sourceforge.net",
    author            = "Gerard Vermeulen",
    author_email      = "gvermeul@grenoble.cnrs.fr",
    license           = "GPL",
    long_description  = long_description,
    platforms         = "Unix, Windows (MSVC)",
    ext_modules       = ext_modules,
    data_files        = data_files,
    scripts           = scripts,
    )

# For in place testing on Posix:
if os.name == 'posix':
    for dir in ['examples', 'junk']:
        if not os.path.exists(dir):
            continue
        os.chdir(dir)
        for lib in glob.glob('../build/lib*-%s.%s/*' % sys.version_info[:2]):
            link = lib.split(os.sep)[-1]
            if os.path.islink(link):
                os.remove(link)
            os.symlink(lib, link)
        os.chdir(os.pardir)
else:
    print "FIXME"

# Local Variables: ***
# compile-command: "python setup.py build" ***
# End: ***
