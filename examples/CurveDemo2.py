#!/usr/bin/env python

# The Python version of qwt-*/examples/curvdemo2/curvdemo2.cpp,
# using curveData() instead of the un-Pythonic setRawData().


import sys
from qt import *
from qwt import *
from Numeric import *

Size=15
USize=13

class CurveDemo(QFrame):

    def __init__(self, *args):
        apply(QFrame.__init__, (self,) + args)

        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setMidLineWidth(3)

        p = QPalette()
        p.setColor(QPalette.Normal, QColorGroup.Background, QColor(30,30,50))
        self.setPalette(p)
        # make curves and maps
        self.tuples = []
        # curve 1
        curve = QwtCurve()
        curve.setPen(QPen(QColor(150, 150, 200), 2))
        curve.setStyle(QwtCurve.Spline, QwtCurve.Xfy),
        curve.setSymbol(QwtSymbol(
            QwtSymbol.Cross, QBrush(), QPen(Qt.yellow, 2), QSize(7, 7)))
        self.tuples.append((curve,
                            QwtDiMap(0, 100, -1.5, 1.5),
                            QwtDiMap(0, 100, 0.0, 2*pi)))
        # curve 2
        curve = QwtCurve()
        curve.setPen(QPen(QColor(200, 150, 50), 1, Qt.DashDotDotLine))
        curve.setStyle(QwtCurve.Sticks)
        curve.setSymbol(QwtSymbol(
            QwtSymbol.Ellipse, QBrush(Qt.blue), QPen(Qt.yellow), QSize(5, 5)))
        self.tuples.append((curve,
                            QwtDiMap(0, 100, 0.0, 2*pi),
                            QwtDiMap(0, 100, -3.0, 1.1)))
        # curve 3
        curve = QwtCurve()
        curve.setPen(QPen(QColor(100, 200, 150)))
        curve.setStyle(
            QwtCurve.Spline, QwtCurve.Periodic | QwtCurve.Parametric)
        self.tuples.append((curve,
                            QwtDiMap(0, 100, -1.1, 3.0),
                            QwtDiMap(0, 100, -1.1, 3.0)))
        # curve 4
        curve = QwtCurve()
        curve.setPen(QPen(Qt.red))
        curve.setStyle(QwtCurve.Spline)
        curve.setSplineSize(200)
        self.tuples.append((curve,
                            QwtDiMap(0, 100, -5.0, 1.1),
                            QwtDiMap(0, 100, -1.1, 5.0)))
        # data
        self.phase = 0.0
        self.base = arrayrange(0.0, 2.01*pi, 2*pi/(USize-1))
        self.uval = cos(self.base)
        self.vval = sin(self.base)
        self.uval[1::2] *= 0.5
        self.vval[1::2] *= 0.5
        self.newValues()
        # start timer
        self.tid = self.startTimer(250)

    def drawContents(self, painter):
        r = self.contentsRect()
        for curve, xMap, yMap in self.tuples:
            xMap.setIntRange(r.left(), r.right())
            yMap.setIntRange(r.top(), r.bottom())
            curve.draw(painter, xMap, yMap)

    def timerEvent(self, event):
        self.newValues()
        self.repaint()
        
    def newValues(self):
        phase = self.phase
        
        self.xval = arrayrange(0, 2.01*pi, 2*pi/(Size-1))
        self.yval = sin(self.xval - phase)
        self.zval = cos(3*(self.xval + phase))
    
        s = 0.25 * sin(phase)
        c = sqrt(1.0 - s*s)
        u = self.uval
        self.uval = c*self.uval-s*self.vval
        self.vval = c*self.vval+s*u

        self.tuples[0][0].setData(self.yval, self.xval)
        self.tuples[1][0].setData(self.xval, self.zval)
        self.tuples[2][0].setData(self.yval, self.zval)
        self.tuples[3][0].setData(self.uval, self.vval)
        
        self.phase += 2*pi/100
        if self.phase>2*pi:
            self.phase = 0.0


def make():
    demo = CurveDemo()
    demo.resize(300, 300)
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
