#!/usr/bin/env ipython

import sys
from qt import *
from qwt import *

class Compass(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setLineWidth(6)        
        self.setFrameShadow(QwtDial.Raised)
        self.setRose(QwtSimpleCompassRose(8, 2))
        self.scaleDraw().setTickLength(0, 0, 3)
        self.setNeedle(QwtCompassMagnetNeedle(
            QwtCompassMagnetNeedle.TriangleStyle, Qt.blue, Qt.red))
        self.setOrigin(220.0)

    # __init__()

# class Compass


def compass():
    c = Compass()
    c.show()
    return c

# compass()


def test_python():
    result = compass()
    print "Testing 'raw_input()' to make 10 other compasses."
    raw_input('Happy? ')
    result = []
    for i in range(10):
        result.append(compass())
    print "Testing 'a = input(..)'"
    a = input("Type a Python statement, e.g 1+1: ")
    print "a =", a
    print "Now, you can try something like: a = test_python()"
    return result

# test_python()


def test_ipython():
    result = []
    for i in range(10):
        result.append(compass())
    print "Initially, input() and raw_input() are flaky,"
    print "but now you can try something like: a = test_python()"
    return result

# test_python()


# Admire!
if __name__ == '__main__':
    # testing for IPython may be subject to change
    if '__IPYTHON__active' in dir(__builtins__):
        import iqt
        # keep references to the widgets
        references = test_ipython()
    else:
        try:
            # check if ICompass.py is interpreted by something like PyCute
            qApp.argc()
        except RuntimeError:
            # fallback for a Command Line Interpreter
            import iqt
        # keep references to the widgets
        references = test_python()

# Local Variables: ***
# mode: python ***
# End: ***
