#!/usr/bin/env python

from qt import *

if qVersion()[0] == '3':
    from qwt.PyCute3 import PyCute
elif qVersion()[0] == '2':
    from qwt.PyCute2 import PyCute

from Numeric import *
from qwt.qplt import *

p = [
    'x = arange(-2*pi, 2*pi, 0.01)',
    'p = Plot(Curve(x, cos(x), Pen(Magenta,2), "cos(x)"),',
    '         Curve(x, exp(x), Pen(Red), "exp(x)", Right),',
    '         Axis(Right, Logarithmic),',
    '         "PyQwt using Qwt-%s -- http://qwt.sf.net" % QWT_VERSION_STR)',
    'x = x[0:-1:10]',
    'p.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),',
    '       Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))',
    ]

q = [
    'x = arange(-2*pi, 2*pi, 0.01)',
    'q = IPlot(Curve(x, cos(x), Pen(Magenta,2), "cos(x)"),',
    '          Curve(x, exp(x), Pen(Red), "exp(x)", Right),',
    '          Axis(Right, Logarithmic),',
    '          "PyQwt using Qwt-%s -- http://qwt.sf.net" % QWT_VERSION_STR)',
    'x = x[0:-1:10]',
    'q.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),',
    '       Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))',
    ]

g = [
    'result = QPixmap.grabWidget(___w___).save("PyCute.png", "PNG")',
    'sys.exit()',
    ]


def make():
    exec('\n'.join(p+q))
    return p, q


if __name__ == '__main__':
    ___a___ = QApplication(sys.argv)

    # locals = .. -- make all names in __main__ visible to the PyCute shell
    # log    = .. -- save session in 'log'
    ___w___ = PyCute(locals=sys.modules['__main__'].__dict__, log='log')
    ___a___.setMainWidget(___w___)
    ___w___.show()

    if (len(sys.argv)) > 1:
        if sys.argv[1] == '--demo':
            ___w___.fakeUser(p+q)
        if sys.argv[1] == '--grab':
            ___w___.resize(600, 180)
            ___w___.fakeUser(p+g)
        else:
            # have to check if argument is python file
            sys.argv = sys.argv[1:]
            ___w___.fakeUser(["execfile('%s')" % sys.argv[0]])
            
    # User, it is your turn!
    ___a___.exec_loop()
