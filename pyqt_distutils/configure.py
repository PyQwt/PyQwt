"""pyqt_distutils.configure

Finds, caches and provides configuration information.
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


__all__ = ['get_config']

import glob, os, sys

from distutils.dir_util import mkpath
from distutils.spawn import find_executable
from distutils.errors import DistutilsFileError, DistutilsPlatformError
from distutils.sysconfig import get_config_var, get_python_inc

from sysconfig import *


def get_config(name):
    """Get the configuration information for package 'name'.

    This function is meant to be the only entry point into this module.
    
    The information is returned in a dictionary, generated on the first
    demand and cached for subsequent demands.
    """

    return {
        'ccache': CCacheInfo,
        'numarray': NumarrayInfo,
        'numeric': NumericInfo,
        'pyqt': PyQtInfo,
        'qt': QtInfo,
        'qt_module': QtModuleInfo,
        'qtgl_module': QtglModuleInfo,
        'qtcanvas_module': QtcanvasModuleInfo,
        'qtext_module': QtextModuleInfo,
        'qwt_module': QwtModuleInfo, # FIXME: returns to many libraries
        'sip': SipInfo,
        }.get(name.lower(), ConfigInfo)().get_info()

# get_info()


class ConfigError(Exception):
    """
    Configuration error.
    """

    def __init__(self):
        Exception.__init__(self)

    # __init__()
    
    def __str__(self):
        return self.__doc__ % self.__dict__

    # __str__()
    
# class ConfigError
    

class MissingFileError(ConfigError):
    """
    File %(file)s does not exist.
    """

    def __init__(self, file):
        ConfigError.__init__(self)
        self.file = file

    # __init__()
    
# class MissingFileError


class MissingProgramError(ConfigError):
    """
    Failed to find %(program)s in %(path)s.

    Directories to search for %(program)s can be specified by setting the
    environment variable %(variable)s.
    """

    def __init__(self, program, path, variable):
        ConfigError.__init__(self)
        self.program = program
        self.path = path
        self.variable = variable

    # __init__()

# class MissingProgramError


class MissingPyQtError(ConfigError):
    """Failed to find PyQt.

    Install or reinstall PyQt for %(python)s.
    """

    def __init__(self, python=sys.executable):
        ConfigError.__init__(self)
        self.python = python

# class MissingPyQtError


class MissingQtError(ConfigError):
    """
    Failed to find Qt.
    
    Set environment variable QTDIR to the Qt root directory. For example:
    (1) for Windows:\n\tset QTDIR=C:\QT
    (2) for bash & friends:\n\texport QTDIR=/usr/lib/qt3
    (3) for csh & friends:\n\tsetenv QTDIR /usr/lib/qt3
    """

# class MissingQtError


class MissingTMakeConfError(ConfigError):
    """
    Failed to find 'tmake.conf' for tmake.
    
    Set environment variable TMAKEPATH. For example:
    (1) for Windows:\n\tset TMAKEPATH=C:\\qt\\tmake\\lib\\win32-msvc
    (2) for bash & friends:\n\texport TMAKEPATH=/usr/lib/tmake/lib/linux-g++
    (3) for csh & friends:\n\tsetenv TMAKEPATH /usr/lib/tmake/lib/linux-g++
    """

# class MissingTMakeConfError


class MissingQMakeConfError(ConfigError):
    """
    Failed to find 'qmake.conf' for tmake or qmake.
    
    Set environment variable QMAKESPEC. For example:
    (1) for Windows:\n\tset QMAKESPEC=win32-msvc
    \tset QMAKESPEC=win32-msvc.net
    (2) for bash & friends:\n\texport QMAKESPEC=linux-g++
    (3) for csh & friends:\n\tsetenv QMAKESPEC irix-n32
    """

# class MissingQMakeConfError


class MatchingSipError(ConfigError):
    """
    '%(source)s' has not been generated with SIP %(sip_version)s.

    PyQt and PyQt based packages should all be generated with the same
    version of SIP.  You actions are:
    - set the environment variable 'SIP_BINDIR' to '/a/suitable/path'
    - python setup.py run_sip --sip-program=/a/suitable/path/sip
    - fix your PyQt and sip installation.
    """

    def __init__(self, source, sip_version):
        ConfigError.__init__(self)
        self.source = source
        self.sip_version = sip_version

    # __init__()

# class MatchingSipError


class NumericConfigError(ConfigError):
    """
    The python package 'Numeric' is broken.

    You should be able to do from the Python interpreter:
    >>> import Numeric
    >>> Numeric.__version__
    and the file '%(array_header)s' should exist

    See http://www.numpy.org for source code to fix 'Numeric'.
    """

    def __init__(self, array_header):
        ConfigError.__init__(self)
        self.array_header = array_header

    # __init__()

# class NumericConfigError


class NumarrayConfigError(ConfigError):
    """
    The python package 'numarray' is broken.

    You should be able to do from the Python interpreter:
    >>> import numarray
    >>> numarray.__version__
    and the file '%(array_header)s' should exist

    See http://www.numpy.org for source code to fix 'numarray'. 
    """

    def __init__(self, array_header):
        ConfigError.__init__(self)
        self.array_header = array_header

    # __init__()
    
# class NumarrayConfigError


class ConfigInfo:
    env_var = None
    verbose = 1
    cache = {}
    
    def __init__(
        self,
        include_dirs=[],
        library_dirs=[],
        program_dirs=os.environ['PATH'].split(os.pathsep)
        ):
        self.defaults = {
            'library_dirs': os.pathsep.join(library_dirs),
            'include_dirs': os.pathsep.join(include_dirs),
            'program_dirs': os.pathsep.join(program_dirs),
            }

    # __init__()

    def calc_info(self):
        if self.verbose:
            print (
                "Use of a no-operation base class '%s'.\n"
                "Hint:\n"
                "- derive a class from '%s',\n"
                "- with a method '%s',\n"
                "- and adapt the function '%s.%s'.\n"
                % (self.__class__, self.__class__, self.calc_info.__name__,
                   __name__, get_config.__name__)
                )
        pass

    # calc_info()
    
    def set_info(self, **info):
        self.cache[self.__class__.__name__] = info

    # set_info()

    def has_info(self):
        return self.cache.has_key(self.__class__.__name__)

    # has_info()

    def get_info(self):
        announce = 0
        if not self.has_info():
            announce = 1
            self.calc_info()
            if self.verbose:
                if not self.has_info():
                    print 'Config failed -- %s.' % self.__class__.__name__
                    self.set_info()
                else:
                    print 'Config succeeded -- %s:' % self.__class__.__name__
        result = self.cache.get(self.__class__.__name__).copy()
        if self.verbose and announce:
            for key, value in result.items():
                print "%s = %s" % (key, value)
            print
        return result

    # get_info()

    def get_paths(self, key):
        result = self.defaults[key].split(os.pathsep)
        if os.environ.has_key(self.env_var):
            for d in os.environ[self.env_var].split(os.pathsep):
                if os.path.isdir(d) and d not in result:
                    result.append(d)
        return result

    # get_paths()

    def get_include_dirs(self, key='include_dirs'):
        return self.get_paths(key)

    # get_include_dirs()
    
    def get_library_dirs(self, key='library_dirs'):
        return self.get_paths(key)

    # get_library_dirs()

    def get_program_dirs(self, key='program_dirs'):
        return self.get_paths(key)

    # get_program_dirs()

# class ConfigInfo


class NumarrayInfo(ConfigInfo):

    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
    
    def calc_info(self):
        array = os.path.join(get_python_inc(), 'numarray', 'arrayobject.h')
        try:
            import numarray
            if os.path.exists(array):
                self.set_info(**{
                    'define_macros': [('HAS_NUMARRAY', None)],
                    'numarray_version': numarray.__version__,
                    })
            else:
                raise NumarrayConfigError(array)
        except ImportError:
            self.set_info(**{})

    # calc_info()

# class NumericInfo


class CCacheInfo(ConfigInfo):
    env_var = 'CCACHE_BINDIR'

    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
    
    def calc_info(self):
        path = os.pathsep.join(self.get_program_dirs())
        ccache_program = find_executable('ccache', path) or ''

        self.set_info(**{
            'ccache_program': ccache_program,
            })
        
    # calc_info()

# class NumericInfo


class NumericInfo(ConfigInfo):

    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
    
    def calc_info(self):
        array = os.path.join(get_python_inc(), 'Numeric', 'arrayobject.h')
        try:
            import Numeric
            if os.path.exists(array):
                self.set_info(**{
                    'define_macros': [('HAS_NUMERIC', None)],
                    'numeric_version': Numeric.__version__,
                    })
            else:
                raise NumericConfigError(array)
        except ImportError:
            self.set_info(**{})

    # calc_info()

# class NumericInfo


class PyQtInfo(ConfigInfo):

    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
    
    def calc_info(self):
        try:
            import qt
        except ImportError:
            raise MissingPyQtError

        self.set_info(**{
            'pyqt_version': qt.PYQT_VERSION,
            'qt_version': qt.QT_VERSION,
            'qt_version_str': qt.QT_VERSION_STR,
            })

    # calc_info()

# class PyQtInfo


class QtModuleInfo(ConfigInfo):
    module = 'qt'

    def __init__(self):
        ConfigInfo.__init__(self)
        self.check_sip_version()

    # __init__()

    def check_sip_version(self):
        source = __import__(self.module).__file__
        if source[-1] == 'c' or source[-1] == 'o':
            source = source[:-1]
        assert source[-2:] == 'py'
        sip_version = get_config('sip')['sip_version']
        if -1 == open(source).read().find(sip_version):
            raise MatchingSipError(source, sip_version)

    # check_sip_version()

    def calc_info(self):
        library_dirs = []
        libraries = []

        if os.name == 'nt':
            template = "%s -vEc __import__('%s')"
            prefix = ''
        elif os.name == 'posix':
            template = "%s -vEc 'import %s'"
            prefix = 'lib'

        _, _, stderr = os.popen3(template % (sys.executable, self.module))
        lines = stderr.readlines()
        skip = 1
        for line in lines:
            line = line.strip()
            if skip:
                if line[:6] == 'Python':
                    skip = 0
            elif -1 < line.find('# dynamically loaded from'):
                library_dir, library = os.path.split(line.split()[-1])
                library, extension = os.path.splitext(library)
                if prefix:
                    library = library.replace(prefix, '', 1)
                if library_dir not in library_dirs:
                    library_dirs.append(library_dir)
                if library not in libraries:
                    libraries.append(library)

        self.set_info(**{
            'libraries': libraries,
            'library_dirs': library_dirs,
            })

    # calc_info()

# class QtModuleInfo


class QtcanvasModuleInfo(QtModuleInfo):
    module = 'qtcanvas'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtCanvasModuleInfo


class QtextModuleInfo(QtModuleInfo):
    module = 'qtext'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtextModuleInfo


class QtglModuleInfo(QtModuleInfo):
    module = 'qtgl'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtglModuleInfo


class QtnetworkModuleInfo(QtModuleInfo):
    module = 'qtnetwork'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtnetworkModuleInfo


class QtsqlModuleInfo(QtModuleInfo):
    module = 'qtsql'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtnetworkModuleInfo


class QttableModuleInfo(QtModuleInfo):
    module = 'qttable'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QttableModuleInfo


class QtxmlModuleInfo(QtModuleInfo):
    module = 'qtxml'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QtxmlModuleInfo


class QwtModuleInfo(QtModuleInfo):
    module = 'qwt'
    
    def __init__(self):
        QtModuleInfo.__init__(self)

    # __init__()

# class QwtModuleInfo


class QtInfo(ConfigInfo):
    
    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
        
    def calc_info(self):
        qtdir = os.environ.get('QTDIR')
        if not qtdir:
            raise MissingQtError

        qtbindir = os.environ.get('QTBINDIR') or os.path.join(qtdir, 'bin')
        qtincdir = os.environ.get('QTINCDIR') or os.path.join(qtdir, 'include')
        qtlibdir = os.environ.get('QTLIBDIR') or os.path.join(qtdir, 'lib')

        qt_version_str = get_qt_version_str(qtincdir)
        sip_t_options = get_sip_t_options(qt_version_str, os.name)
        tag = qt_version_str.replace('.', '')

        define_macros = [
            ('NDEBUG', None),
            ('QT_NODEBUG', None),
            ]
        include_dirs = []
        library_dirs = []
        libraries = []
        
        if qt_version_str[0] == '2':
            tmakepath = os.environ.get('TMAKEPATH') or ''
            tmakeconf = os.path.join(tmakepath, 'tmake.conf')
            if not os.path.exists(tmakeconf):
                raise MissingTMakeConfError
            make = get_tmake_conf_info(tmakeconf, qtdir)
            type = more_tmake_conf_info(make, qtlibdir, tag)
        elif qt_version_str[0] == '3':
            qmakespec = os.environ.get('QMAKESPEC') or ''
            for qmakeconf in [
                # recommended in Qt-3.x documentation
                os.path.join(qtdir, 'mkspecs', qmakespec, 'qmake.conf'),
                # qmake also accepts a full path name (tmake compatible)
                os.path.join(qmakespec, 'qmake.conf'),
                # vanilla Qt-3.x has a symbolic link to QMAKESPEC
                os.path.join(qtdir, 'mkspecs', 'default', 'qmake.conf'),
                # sentinel
                '']:
                if os.path.exists(qmakeconf):
                    break
            if not qmakeconf:
                raise MissingQMakeConfError
            make = get_qmake_conf_info(qmakeconf, qtdir)
            type = more_qmake_conf_info(make, qtlibdir, tag)

        include_dirs.append(make['INCDIR_QT'])
        library_dirs.append(make['LIBDIR_QT'])
        if os.name == 'nt':
            define_macros.append(('QT_DLL', None))
            define_macros.append(('QT_THREAD_SUPPORT', None))
            libraries.append(make['LIBS_QT_THREAD'])
        elif os.name == 'posix':
            if 'thread' in type:
                libraries.append(make['LIBS_QT_THREAD'])
                libraries.append(make['LIBS_THREAD'])
                define_macros.append(('QT_THREAD_SUPPORT', None))
            else:
                libraries.append(make_info['LIBS_QT'])
            # normalize, chop of the leading '-l'
            libraries = [ lib[2:] for lib in ' '.join(libraries).split()]
            
        
        self.set_info(**{
            'qt_version_str': "%s" % qt_version_str,
            'sip_t_options': sip_t_options,
            'make': make,
            'type': type,
            'qtdir': qtdir,
            'qtbindir': qtbindir,
            'qtincdir': qtincdir,
            'qtlibdir': qtlibdir,
            'define_macros': define_macros,
            'include_dirs': include_dirs,
            'library_dirs': library_dirs,
            'libraries': libraries,
            })

    # calc_info()

# class QtInfo


class SipInfo(ConfigInfo):
    env_var = 'SIP_BINDIR'

    def __init__(self):
        ConfigInfo.__init__(self)

    # __init__()
        
    def calc_info(self):
        path = os.pathsep.join(self.get_program_dirs())
        sip_program = find_executable('sip', path)
        if not sip_program:
            raise MissingProgramError('sip', path, self.env_var)
        sip_version = os.popen('%s -V' % sip_program).read().rstrip()

        define_macros = []

        mkpath('.configure')
        os.popen('%s -c .configure' % sip_program, 'w').write(
            '%Module Module\n int Int;\n')
        text = open(os.path.join('.configure', 'sipModuleDeclModule.h')).read()
        if -1 != text.find('sipName_Module_Int'):
            define_macros.append(('OLD_SIP_NAMES', None))
        if os.name == 'nt':
            define_macros.append(('SIP_MAKE_MODULE_DLL', None))
        
        sip_x_features = []
        from qt import QObject
        if 'className' in dir(QObject):
            sip_x_features.extend(['-x', 'SIP_DUMB_DIR'])

        self.set_info(**{
            'sip_version': sip_version,
            'define_macros': define_macros,
            'sip_program': sip_program,
            'sip_x_features': sip_x_features,
            })
        
    # calc_info()

# class SipInfo


def get_sip_t_options(qt_version_str, os_name):
    """Return the Qt version and Window system related options for sip.
    """
    qt = {
        '2.3.0': 'Qt_2_3_0',
        '2.3.1': 'Qt_2_3_1',
        '2.3.2': 'Qt_2_3_1',
        '3.0.0': 'Qt_3_0_0',
        '3.0.1': 'Qt_3_0_1',
        '3.0.2': 'Qt_3_0_2',
        '3.0.3': 'Qt_3_0_2',
        '3.0.4': 'Qt_3_0_4',
        '3.0.5': 'Qt_3_0_5',
        '3.0.6': 'Qt_3_0_6',
        '3.0.7': 'Qt_3_0_6',
        '3.1.0': 'Qt_3_1_0',
        '3.1.1': 'Qt_3_1_1',
        '3.1.2': 'Qt_3_1_2',
        '3.2.0': 'Qt_3_2_0',
        }.get(qt_version_str)

    if not qt:
        raise SystemExit, ("Qt-%s is unsupported." % qt_version_str)

    ws = {
        'nt': 'WS_WIN',
        'posix': 'WS_X11',
        }.get(os_name)

    if not ws:
        raise OSError(os_name)

    return ['-t', qt, '-t', ws]

# get_sip_qt_ws_options()


def get_qt_version_str(qtincdir):
    """Get the first 5 characters of QT_VERSION_STR from 'qglobal.h'
    """
    header = os.path.join(qtincdir, 'qglobal.h')
    if not os.path.exists(header):
        raise MissingFileError(header)
    qt_version_str = ''
    for line in file(header).readlines():
        words = line.split()
        if len(words) == 3 and words[0] == '#define':
            if words[1] == 'QT_VERSION_STR':
                qt_version_str = words[2][1:-1]
        if qt_version_str:
            break
    return qt_version_str[:5]

# get_qt_version_str()


def get_qmake_conf_info(qmakeconf, qtdir):
    info = {}
    for line in file(qmakeconf).readlines():
        if line[:5] == 'QMAKE':
            split = line.find('=')
            key = line[:split].strip()[6:]
            value = line[split+1:].strip()
            if value[:2] == "$$":
                macro = value.split()[0]
                value = value.replace(macro, info[macro[8:]])
            info[key] = value.replace('$(QTDIR)', qtdir)
    return info

# get_qmake_conf_info()


def more_qmake_conf_info(info, qtlibdir, tag='', platform=None):
    if not platform:
        platform = os.name
    if platform == 'nt':
        # qmake.conf's library names seem incomplete
        globs = glob.glob(os.path.join(qtlibdir, 'qt-mt%s*.lib' % tag))
        if not globs:
            raise DistutilsFileError, "Failed to find the Qt library"
        type = ['thread']
        library_dir, library = os.path.split(
            os.path.splitext(globs[0])[0])
        info['LIBS_QT_THREAD'] = library
        if not info.has_key('LIBDIR_QT'):
            info['LIBDIR_QT'] = library_dir                
    elif platform == 'posix':
        if glob.glob(os.path.join(qtlibdir, "libqt-mt.so*")):
            type = ['thread']
        elif glob.glob(os.path.join(qtlibdir, "libqt.so*")):
            type = []
        else:
            raise DistutilsFileError, "Failed to find the Qt library"
    else:
        raise DistutilsPlatformError, "'%s' is not supported." % platform
    return type

# more_qmake_conf_info()


def get_tmake_conf_info(tmakeconf, qtdir):
    info = {}
    for line in file(tmakeconf).readlines():
        if line[:5] == 'TMAKE':
            split = line.find('=')
            key = line[:split].strip()[6:]
            value = line[split+1:].strip()
            if value[:2] == "$$":
                value = info[value[8:]]
            info[key] = value.replace('$(QTDIR)', qtdir)
    return info

# get_tmake_conf_info()


def more_tmake_conf_info(info, qtlibdir, tag='', platform=None):
    if not platform:
        platform = os.name
    if platform == 'nt':
        # tmake.conf in Qt-2.3.0-NC is impaired
        globs = glob.glob(os.path.join(qtlibdir, 'qt-mt%s*.lib' % tag))
        if globs:
            type = ['thread']
        else:
            raise DistutilsFileError, "Failed to find the Qt library"
        library_dir, library = os.path.split(os.path.splitext(globs[0])[0])
        info['LIBS_QT_THREAD'] = library
        info['LIBDIR_QT'] = library_dir                
    elif platform == 'posix':
        if glob.glob(os.path.join(qtlibdir, "libqt-mt.so*")):
            type = ['thread']
        elif glob.glob(os.path.join(qtlibdir, "libqt.so*")):
            type = []
        else:
            raise DistutilsFileError, "Failed to find the Qt library"
        if not info.has_key('LFLAGS_PLUGIN'):
            info['LFLAGS_PLUGIN'] = info['LFLAGS_SHLIB']
    else:
        raise DistutilsPlatformError, "'%s' is not supported." % platform
    return type

# more_tmake_conf_info()


def show_all():
    for item in [
        'pyqt',
        'qt',
        'sip',
        'numarray',
        'numeric',
        'qt_module',
        'qwt_module',
        'pipo']:
        get_config(item)

# show_all()


if __name__ == '__main__':
    show_all()
    
# Local Variables: ***
# mode: python ***
# End: ***
