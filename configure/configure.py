# Generate the build tree and Makefiles for PyQwt.
#
#
# Copyright (C) 2004 Gerard Vermeulen
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

import cStringIO
import compileall
import getopt
import glob
import os
import shutil
import sys

import sipconfig
import pyqtconfig

# Initialise the globals.
pyqwt_version = 0x040000
pyqwt_version_str = "4.0"

pyqwt_packages = ["qwt"]
pyqwt_defines = []
pyqwt_extra_python_files = glob.glob(os.path.join(os.pardir, 'qwt', '*.py'))
qwt_sip_flags = []

sip_min_v3_version = 0x030a00
sip_min_v4_version = 0x040000

# Get the pyqt configuration.
pyqtcfg = pyqtconfig.Configuration()

if pyqtcfg.qt_version == 0:
    sipconfig.error("SIP has been built with Qt support disabled.")

# Command line options.
opt_pyqwtpkgdir = os.path.join(pyqtcfg.default_mod_dir)
opt_pyqwtsipdir = pyqtcfg.default_sip_dir
opt_pyqtmoddir = pyqtcfg.pyqt_mod_dir
opt_pyqtsipdir = pyqtcfg.pyqt_sip_dir
opt_debug = 0
opt_concat = 0
opt_split = 1
opt_releasegil = 0
opt_tracing = 0

opt_qwtincdir = None
opt_qwtlibdir = None

def usage(rcode = 2):
    """Display a usage message and exit.

    rcode is the return code passed back to the calling process.
    """
    if pyqtcfg.sip_version < 0x040000:
        add_opt = "[-p dir] "
    else:
        add_opt = ""
    print "Usage:"
    print "    python configure.py [-h] [-c] [-d dir] [-g] [-i dir] [-j #] [-l dir] [-r] [-u] [-v dir] [-x dir]", add_opt
    print "where:"
    print "    -h      display this help message"
    print "    -c      concatenate C/C++ source files for each module"
    print "    -d dir  install directory for the PyQwt packages [default %s]" % opt_pyqwtpkgdir
    print "    -g      always release the GIL (SIP v3.x behaviour)"
    print "    -i dir  directory containing the Qwt include files [default %s]" % opt_qwtincdir
    print "    -j #    split the concatenated C++ source files into # pieces [default 1]"
    print "    -l dir  directory containing the Qwt library [default %s]" % opt_qwtlibdir
    print "    -r      generate code with tracing enabled [default disabled]"
    print "    -u      build with debugging symbols"
    print "    -v dir  install directory for the PyQwt .sip files [default %s]" % opt_pyqwtsipdir
    print "    -x dir  directory containing the PyQt sip files [default %s]" % opt_pyqtsipdir
    if pyqtcfg.sip_version < 0x040000:
        print "    -p dir  directory containing the PyQt libraries [default %s]" % opt_pyqtmoddir

    sys.exit(rcode)

# usage()

def inform_user():
    """Tell the user the option values that are going to be used.
    """
    sipconfig.inform("These PyQwt packages will be built: %s."
                     % ' '.join(pyqwt_packages))
    sipconfig.inform("The PyQwt packages will be installed in %s."
                     % opt_pyqwtpkgdir)
    sipconfig.inform("The PyQwt .sip files will be installed in %s."
                     % opt_pyqwtsipdir)

# inform_user()

def create_config(module, template):
    """Create the PyQwt configuration module for use in build scripts.

    module is the module file name.
    template is the template file name.
    """
    sipconfig.inform("Creating %s..." % module)

    content = {
        "pyqwt_version":        pyqwt_version,
        "pyqwt_version_str":    pyqwt_version_str,
        "pyqwt_pkg_dir":        opt_pyqwtpkgdir,
        "pyqwt_sip_dir":        opt_pyqwtsipdir,
        "pyqwt_modules":        pyqwt_packages,
        "pyqwt_qwt_sip_flags":  qwt_sip_flags,
        "pyqwt_defines":        pyqwt_defines
    }

    sipconfig.create_config_module(module, template, content)

# create_config()

def check_readline():
    try:
        pyqwt_packages.append('iqt')
    except ImportError:
        pass

# check_readline()

def check_numarray():
    """See if the numarray extension has been installed.
    """
    try:
        import numarray
        # Try to find Numeric/libnumarray.h.
        numarray_inc = os.path.join(
            pyqtcfg.py_inc_dir, "numarray", "libnumarray.h")
        if os.access(numarray_inc, os.F_OK):
            sipconfig.inform(
                "numarray-%s is being used." % numarray.__version__)
            pyqwt_defines.append("HAS_NUMARRAY")
        else:
            sipconfig.inform(
                "numarray has been installed, "
                "but its headers are not in the standard location.\n"
                "PyQwt will be build without support for numarray.\n"
                "(Linux users may have to install a development package)"
                )
            raise ImportError
    except ImportError:
        qwt_sip_flags.append("-x")
        qwt_sip_flags.append("HAS_NUMARRAY")
        sipconfig.inform(
            "Failed to import numarray: "
            "PyQwt will be build without support for numarray."
            )

# check_numarray()

def check_numeric():
    """See if the Numeric extension has been installed.
    """
    try:
        import Numeric
        # Try to find Numeric/arrayobject.h.
        numeric_inc = os.path.join(
            pyqtcfg.py_inc_dir, "Numeric", "arrayobject.h")
        if os.access(numeric_inc, os.F_OK):
            sipconfig.inform(
                "Numeric-%s will be used." % Numeric.__version__)
            pyqwt_defines.append("HAS_NUMERIC")
        else:
            sipconfig.inform(
                "Numeric has been installed, "
                "but its headers are not in the standard location.\n"
                "PyQwt will be build without support for Numeric."
                "(Linux users may have to install a development package)"
                )
            raise ImportError
    except ImportError:
        qwt_sip_flags.append("-x")
        qwt_sip_flags.append("HAS_NUMERIC")
        sipconfig.inform(
            "Failed to find Numeric: "
            "PyQwt will be build without support for Numeric."
            )

# check_numeric()

def check_dynamic_cast():
    program = (
        "class a { public: virtual void v() = 0; virtual ~a() {}; };\n"
        "class b: public a { public: virtual void v() {}; virtual ~b() {} };\n"
        "int main() { a *o = new b; dynamic_cast<const b *>(o); return 0; }\n"
        )
    name = "test.cpp"
    open(name, "w").write(program)
    makefile = sipconfig.ProgramMakefile(pyqtcfg, console=1)
    exe, build = makefile.build_command(name)
    try:
        os.remove(exe)
    except OSError:
        pass
    print "Check if your PyQt setup handles 'dynamic_cast<>()'"
    os.system(build)
    try:
        os.remove(exe)
        print "YES"
    except OSError:
        qwt_sip_flags.append("-x")
        qwt_sip_flags.append("CXX_DYNAMIC_CAST")
        print "NO"
        
# check_dynamic_cast

def check_types():
    program = (
        "#include <stddef.h>\n"
        "class a { public: void f(size_t); };\n"
        "void a::f(%s) {};\n"
        "int main() { return 0; }\n"
        )
    name = "test.cpp"
    makefile = sipconfig.ProgramMakefile(pyqtcfg, console=1)
    exe, build = makefile.build_command(name)
    try:
        os.remove(exe)
    except OSError:
        pass

    new = cStringIO.StringIO()
    print >> new, '// Automagically generated by configure.py'
    print >> new
    print >> new, '// Uncomment one of the following four lines'

    for ctype in ('int', 'long', 'unsigned int', 'unsigned long'):
        open(name, "w").write(program % ctype)
        print "Check if 'size_t' and '%s' are the same type." % ctype
        os.system(build)
        try:
            os.remove(exe)
            comment = ''
            print "YES"
        except OSError:
            print "NO"
            comment =  '//'
        print >> new, '%stypedef %s size_t;' % (comment, ctype)

    print >> new
    print >> new, '// Local Variables:'
    print >> new, '// mode: C++'
    print >> new, '// c-file-style: "stroustrup"'
    print >> new, '// End:'

    types_sip = os.path.join(os.pardir, 'sip', 'types.sip')
    if os.access(types_sip, os.R_OK):
        old = open(types_sip, 'r').read()
    else:
        old = ''
    if old != new.getvalue():
        open(types_sip, 'w').write(new.getvalue())

# check_types()

def set_sip_flags():
    """Set the SIP version flags.
    """
    # Get the PyQt sip flags
    qwt_sip_flags.extend(pyqtcfg.pyqt_qt_sip_flags.split())

        
def generate_code(
    mod_name, mod_builddir, sipfile, imports=[], sip_flags=[], opengl=0,
    extra_cflags=[], extra_cxxflags=[],
    extra_defines=[], extra_include_dirs=[],
    extra_lflags=[], extra_lib_dirs=[], extra_libs=[],
    extra_cpp_files=[], extra_moc_headers=[], extra_python_files=[]
    ):
    """Generate the code for a module.

    mod_name is the name of the module.
    mod_builddir is the directory where to build the module.
    sipfile is the sip file defining the module in the package.
    imports is the list of PyQt modules that this module %Imports.
    sip_flags is a list of sip flags.
    opengl is set if the module needs OpenGL support.
    extra_cflags is a list containing additional C compiler flags.
    extra_cxxflags is a list containing additional C++ compiler flags.
    extra_defines is a list containing additional preprocessor defines.
    extra_include_dirs is a list containing additional include directories.
    extra_lflags is a list containing additional linker flags.
    extra_lib_dirs is a list containing additional library directories.
    extra_libs is a list containing additional libraries.
    extra_cpp_files is a list of additional C++ sources.
    extra_moc_headers is a list of additional header files for moc.
    extra_python_files is a list of additional python files.
    """
    sipconfig.inform("Generating the C++ source for the %s module..."
                     % mod_name)

    try:
        shutil.rmtree(mod_builddir)
    except:
        pass

    try:
        os.mkdir(mod_builddir)
    except:
        sipconfig.error("Unable to create the %s directory." % mod_builddir)

    for file in extra_cpp_files:
        shutil.copy2(file, os.path.join(mod_builddir, os.path.basename(file)))

    for file in extra_moc_headers:
        shutil.copy2(file, os.path.join(mod_builddir, os.path.basename(file)))

    for file in extra_python_files:
        shutil.copy2(file, os.path.join(mod_builddir, os.path.basename(file)))

    # Build the SIP command line.
    argv = [pyqtcfg.sip_bin]

    argv.extend(sip_flags)

    if opt_concat:
        argv.append("-j")
        argv.append(str(opt_split))
        
    if opt_tracing:
        argv.append("-r")

    if opt_releasegil:
        argv.append("-g")

    argv.append("-c")
    argv.append(mod_builddir)

    buildfile = os.path.join(mod_builddir, mod_name + ".sbf")
    argv.append("-b")
    argv.append(buildfile)

    argv.append("-I")
    argv.append("sip")

    # SIP assumes POSIX style path separators.
    argv.append("-I")
    argv.append(opt_pyqtsipdir.replace("\\", "/"))

    argv.append(sipfile.replace("\\", "/"))

    print ' '.join(argv)
    os.system(' '.join(argv))

    # Check the result.
    if not os.access(buildfile, os.F_OK):
        sipconfig.error("Unable to create the C++ code.")

    pyqwtmoddir = os.path.join(opt_pyqwtpkgdir, mod_name)
    compileall.compile_dir(mod_builddir, 1, pyqwtmoddir)

    installs = []
    for file in glob.glob(os.path.join(mod_builddir, '*.py*')):
        installs.append([[os.path.basename(file)], pyqwtmoddir])
    
    # Generate the Makefile.
    sipconfig.inform("Creating the Makefile for the %s module..." % mod_name)

    sipfiles = []

    for file in glob.glob(os.path.join(os.pardir, "sip", "*.sip")):
        sipfiles.append(os.path.join(os.pardir, file))

    installs.append([sipfiles, os.path.join(opt_pyqtsipdir, mod_name)])

    lines = open(buildfile).readlines()
    output = open(buildfile, "w")
    for line in lines:
        if line.startswith('sources'):
            chunks = [line.rstrip()]
            for file in extra_cpp_files:
                chunks.append(os.path.basename(file))
            line = ' '.join(chunks)
        if line.startswith('moc_headers'):
            chunks = [line.rstrip()]
            for file in extra_moc_headers:
                chunks.append(os.path.basename(file))
            line = ' '.join(chunks)
        print >> output, line
            
    output.close()

    makefile = pyqtconfig.QtModuleMakefile(
        configuration = pyqtcfg,
        build_file = mod_name + ".sbf",
        dir = mod_builddir,
        install_dir = pyqwtmoddir,
        installs = installs,
        qt = 1,
        opengl = opengl,
        warnings = 1,
        debug = opt_debug
    )

    if extra_cflags:
        makefile.extra_cflags.extend(extra_cflags)

    if extra_cxxflags:
        makefile.extra_cxxflags.extend(extra_cxxflags)

    if extra_defines:
        makefile.extra_defines.extend(extra_defines)

    if extra_include_dirs:
        makefile.extra_include_dirs.extend(extra_include_dirs)

    if extra_lflags:
        makefile.extra_lflags.append(extra_lflags)

    if extra_lib_dirs:
        makefile.extra_lib_dirs.extend(extra_lib_dirs)

    if extra_libs:
        makefile.extra_libs.extend(extra_libs)

    if pyqtcfg.sip_version < 0x040000 and imports:
        # Inter-module links.
        for im in imports:
            makefile.extra_lib_dirs.insert(0, os.path.join("..", im))
            makefile.extra_libs.insert(0, makefile.module_as_lib(im))

    makefile.generate()


def setup_iqt_build():
    try:
        shutil.rmtree('iqt')
    except:
        pass

    try:
        os.mkdir('iqt')
    except:
        sipconfig.error("Unable to create the iqt directory.")

    files = (
        glob.glob(os.path.join(os.pardir, 'iqt', '*.cpp'))
        + glob.glob(os.path.join(os.pardir, 'iqt', '*.py'))
        + glob.glob(os.path.join(os.pardir, 'iqt', '*.sbf'))
        )

    for file in files:
        shutil.copy2(file, os.path.join('iqt', os.path.basename(file)))

    pyiqtmoddir = os.path.join(opt_pyqwtpkgdir, 'iqt')
    compileall.compile_dir('iqt', 1, pyiqtmoddir)

    sipconfig.inform("Creating the Makefile for the iqt module...")
    makefile = sipconfig.ModuleMakefile(
        configuration = pyqtcfg,
        build_file = 'iqt.sbf',
        dir = 'iqt',
        install_dir = pyiqtmoddir,
        installs = [[['__init__.py', '__init__.pyc'], pyiqtmoddir]],
        qt=1,
        warnings = 1,
        debug = opt_debug
        )

    makefile._target = '_iqt'
    makefile.generate()

# setup_iqt_build()

def setup_build():
    """Create the top level Makefile"""
    sipconfig.inform("Creating top level Makefile...")
    sipconfig.ParentMakefile(
        configuration = pyqtcfg,
        subdirs = pyqwt_packages,
        #installs = ("pyqwtconfig.py", os.path.join('qwt', opt_pyqwtpkgdir)),
    ).generate()
        

def main(argv):
    """Create the configuration module module.

    argv is the list of command line arguments.
    """
    if pyqtcfg.sip_version < 0x040000:
        flags = "hcd:gi:j:l:ruv:p:x:y:"
    else:
        flags = "hcd:gi:j:l:ruv:x:y:"
    try:
        optlist, args = getopt.getopt(argv[1:], flags)
    except getopt.GetoptError:
        usage()

    global opt_pyqwtpkgdir, opt_pyqwtsipdir
    global opt_pyqtmoddir, opt_pyqtsipdir
    global opt_debug, opt_concat, opt_releasegil
    global opt_split, opt_tracing
    global opt_qwtincdir, opt_qwtlibdir

    for opt, arg in optlist:
        if opt == "-h":
            usage(0)
        elif opt == "-c":
            opt_concat = 1
        elif opt == "-d":
            opt_pyqwtpkgdir = arg
        elif opt == "-g":
            opt_releasegil = 1
        elif opt == "-i":
            opt_qwtincdir = arg
        elif opt == "-j":
            try:
                opt_split = int(arg)
            except:
                usage()
        elif opt == "-l":
            opt_qwtlibdir = arg
        elif opt == "-p":
            if pyqtcfg.sip_version < 0x040000:
                opt_pyqtmoddir = arg
            else:
                usage()
        elif opt == "-r":
            opt_tracing = 1
        elif opt == "-u":
            opt_debug = 1
        elif opt == "-v":
            opt_pyqwtsipdir = arg
        elif opt == "-x":
            opt_pyqtsipdir = arg
             
    if args:
        usage()

    sipconfig.inform("SIP %s is being used." % pyqtcfg.sip_version_str)

    # Check if SIP is new enough.
    if pyqtcfg.sip_version_str[:8] != "snapshot":
        minv = None

        if pyqtcfg.sip_version >= 0x040000:
            if pyqtcfg.sip_version < sip_min_v4_version:
                minv = sip_min_v4_version
        else:
            if pyqtcfg.sip_version < sip_min_v3_version:
                minv = sip_min_v3_version

        if minv:
            pyqtcfg.error("This version of PyQwt requires SIP v%s or later"
                          % pyqtcfg.version_to_string(minv))

    # check for readline
    check_readline()

    # check for numarray
    check_numarray()

    # check for Numeric
    check_numeric()

    # check for dynamic_cast
    check_dynamic_cast()

    # check for ISO C types.
    check_types()

    # Set the SIP platform, version and feature flags.
    set_sip_flags()

    # Tell the user what's been found.
    inform_user()

    # Generate the code.
    if opt_qwtincdir:
        extra_include_dirs = [
            os.path.join(opt_qwtincdir),
            os.path.join(os.pardir, os.pardir, 'numpy')
            ]
    else:
        extra_include_dirs = [
            os.path.join(os.pardir, os.pardir, 'qwt-sources', 'include'),
            os.path.join(os.pardir, os.pardir, 'numpy')
            ]
    pyqwt_extra_cpp_files = glob.glob(
        os.path.join(os.pardir, 'numpy', '*.cpp'))

    if opt_qwtlibdir:
        extra_lib_dirs = [opt_qwtlibdir]
        extra_libs = ['qwt']
        pyqwt_extra_moc_headers = []
    else:
        extra_lib_dirs=[]
        extra_libs=[]
        pyqwt_extra_moc_headers = []
        for filename in glob.glob(
            os.path.join(os.pardir, 'qwt-sources', 'include', '*.h')):
            if -1 != open(filename).read().find('Q_OBJECT'):
                pyqwt_extra_moc_headers.append(filename)
        pyqwt_extra_cpp_files += glob.glob(
            os.path.join(os.pardir, 'qwt-sources', 'src', '*.cpp'))

    generate_code(
        'qwt',
        'qwt',
        os.path.join(os.pardir, 'sip', 'qwtmod.sip'),
        imports = ['qt'],
        sip_flags = qwt_sip_flags,
        extra_defines =  pyqwt_defines,
        extra_include_dirs = extra_include_dirs,
        extra_lib_dirs = extra_lib_dirs,
        extra_libs = extra_libs,
        extra_cpp_files = pyqwt_extra_cpp_files,
        extra_moc_headers = pyqwt_extra_moc_headers,
        extra_python_files = pyqwt_extra_python_files,
        )

    setup_iqt_build()

    # Create the additional Makefiles.
    setup_build()

    # Install the configuration module.
    #create_config('pyqwtconfig.py', 'pyqwtconfig.py.in')

    # For in place testing on Posix:
    if os.name == 'posix':
        os.chdir(os.pardir)
        for dir in ['examples', 'junk']:
            if not os.path.exists(dir):
                continue
            os.chdir(dir)
            for lib in glob.glob(os.path.join(os.pardir, 'configure', '*')):
                link = lib.split(os.sep)[-1]
                if not link in ['iqt', 'qwt']:
                    continue
                if os.path.islink(link):
                    os.remove(link)
                os.symlink(lib, link)
            os.chdir(os.pardir)

    print 'Run "make" to compile PyQwt'

###############################################################################
# The script starts here.
###############################################################################

if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit:
        raise
    except:
        print (
            "An internal error occured.  Please report all the output\n"
            "from the program, including the following traceback, to\n"
            "pyqwt-users@lists.sourceforge.net"
            )
        raise

