#!/usr/bin/env python

from qwt.qplt import *

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

def make():
    x = arange(-2*pi, 2*pi, 0.01)
    demo = Plot(Curve(x, cos(x), Pen(Magenta, 2), "cos(x)"),
                Curve(x, exp(x), Pen(Red), "exp(x)", Right),
                Axis(Right, Logarithmic),
                "PyQwt using Qwt-%s -- http://qwt.sf.net" % QWT_VERSION_STR)
    x = x[0:-1:10]
    demo.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),
              Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))
    return demo

# Admire!
if __name__ == '__main__':
    main(sys.argv)
