#!/usr/bin/env python

import sys
from qt import *
from qwt import *

modules = []
for name in ['Numeric', 'numarray']:
    try:
        name = __import__(name)
        modules.append(name)
    except ImportError:
        pass

curve = QwtCurve()
# Check that QwtCurve.setData(x, y) leaves the reference count invariant
for module in modules:
    print 'Check invariance of reference counting the interface to module:'
    print module
    x = module.arange(0.0, 10.0, 1.0)
    y = module.arange(0.0, 10.0, 1.0)
    print sys.getrefcount(x)
    print x
    curve.setData(x, y)
    print sys.getrefcount(x)
    print x
    print '--'
    x = module.array(range(10))
    y = module.array(range(10))
    print x, sys.getrefcount(x), x.typecode()
    curve.setData(x, y)
    print x, sys.getrefcount(x), x.typecode()
    print '--'
    x = module.array([range(10), range(10)])
    y = module.array([range(10), range(10)])
    print x, sys.getrefcount(x), x.typecode()
    curve.setData(x, y)
    print x, sys.getrefcount(x), x.typecode()
    print '--'
    print '-------------------------------------------------------------------'
    print
# To trace refcounts in sip generated code, use something like:
#       #include <iostream.h>
#       PyObject *refCounted;
#       cout >> refCounted->ob_refcnt >> endl;
#
# Do not use printf(), because sip chokes on %.
