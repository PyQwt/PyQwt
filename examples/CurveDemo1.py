#!/usr/bin/env python

# The Python version of qwt-*/examples/curvedemo1/curvdemo1.cpp

# This examples demonstrate the use of keyword arguments in constructors, like:
#
# instance = ClassName(keyword1 = value1, keyword2 = value2, ..).
#
# Any method name can be used as a keyword. The value is a Python object,
# whose type depend on the method name (the object can be a tuple, if the
# method takes more than one argument).
#
# The keyword arguments feature is enabled by
# post-processing sip-generated *.py files.
#
# Warning: this feature is a HACK, only working in constructors!
# Qt's Designer and pyuic don't know about keyword arguments.
# If you code by hand, keyword arguments allow for shorter code.

import sys
from qt import *
from qwt import *
from Numeric import *

SIZE=27

class CurveDemo(QFrame):

    def __init__(self, *args):
        apply(QFrame.__init__, (self,) + args)

        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        # make curves with different styles
        self.curves = []
        # curve 0
        curve = QwtCurve()
        curve.setPen(QPen(Qt.darkGreen))
        curve.setStyle(QwtCurve.Spline)
        curve.setSymbol(QwtSymbol(QwtSymbol.Cross, QBrush(),
                                  QPen(Qt.black), QSize(5, 5)))
        self.curves.append(curve)
        # curve 1
        curve = QwtCurve()
        curve.setPen(QPen(Qt.red))
        curve.setStyle(QwtCurve.Sticks)
        curve.setSymbol(QwtSymbol(QwtSymbol.Ellipse, QBrush(Qt.yellow),
                                  QPen(Qt.blue), QSize(5, 5)))
        self.curves.append(curve)
        # curve 2
        curve = QwtCurve()
        curve.setPen(QPen(Qt.darkBlue))
        curve.setStyle(QwtCurve.Lines)
        self.curves.append(curve)
        # curve 3
        curve = QwtCurve()
        curve.setPen(QPen(Qt.darkCyan))
        curve.setStyle(QwtCurve.Steps)
        self.curves.append(curve)
        # curve 4
        curve = QwtCurve()
        curve.setStyle(QwtCurve.NoCurve)
        curve.setSymbol(QwtSymbol(QwtSymbol.XCross, QBrush(),
                                  QPen(Qt.darkMagenta), QSize(5, 5)))
        self.curves.append(curve)

        # attach data, using Numeric
        self.x = arrayrange(0, 10.0, 10.0/SIZE)
        self.y = sin(self.x)*cos(2*self.x)
        for curve in self.curves:
            curve.setData(self.x, self.y)
        self.xMap = QwtDiMap()
        self.xMap.setDblRange(-0.5, 10.5)
        self.yMap = QwtDiMap()
        self.yMap.setDblRange(-1.1, 1.1)


    def drawContents(self, painter):
        # draw curves
        r = self.contentsRect()
        dy = r.height()/len(self.curves)
        r.setHeight(dy)
        for curve in self.curves:
            self.xMap.setIntRange(r.left(), r.right())
            self.yMap.setIntRange(r.top(), r.bottom())
            curve.draw(painter, self.xMap, self.yMap)
            r.moveBy(0, dy)
        # draw titles
        r = self.contentsRect()
        r.setHeight(dy)
        painter.setFont(QFont('Helvetica', 8))
        painter.setPen(Qt.black)
        titles = [ 'Style: Spline, Symbol: Cross',
                   'Style: Sticks, Symbol: Ellipse',
                   'Style: Lines, Symbol: None',
                   'Style: Steps, Symbol: None',
                   'Style: NoCurve, Symbol: XCross' ]
        for title in titles:
            painter.drawText(
                0, r.top(), r.width(), painter.fontMetrics().height(),
                Qt.AlignTop | Qt.AlignHCenter, title)
            r.moveBy(0, dy)


def make():
    demo = CurveDemo()
    demo.resize(300, 600)
    demo.show()
    return demo

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()    

# Admire!         
if __name__ == '__main__':
    main(sys.argv)
