#!/usr/bin/env python

# The Python version of qwt-*/examples/data_plot/data_plot.cpp

import random, sys
from qt import *
from qwt import *
from Numeric import *


class DataPlot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        # Initialize data
        self.x = arrayrange(0.0, 100.1, 0.5)
        self.y = zeros(len(self.x), Float)
        self.z = zeros(len(self.x), Float)

        self.setTitle("A Moving QwtPlot Demonstration")
        self.setAutoLegend(True)

        self.curveR = self.insertCurve("Data Moving Right")
        self.curveL = self.insertCurve("Data Moving Left")

        self.setCurveSymbol(self.curveL, QwtSymbol(
            QwtSymbol.Ellipse, QBrush(), QPen(Qt.yellow), QSize(7, 7)))

        self.setCurvePen(self.curveR, QPen(Qt.red))
        self.setCurvePen(self.curveL, QPen(Qt.blue))

        mY = self.insertLineMarker("", QwtPlot.yLeft)      
        self.setMarkerYPos(mY, 0.0)

        self.setAxisTitle(QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(QwtPlot.yLeft, "Values")
    
        self.startTimer(50);
        self.phase = 0.0

    # __init__()
    
    def timerEvent(self, e):
        if self.phase > pi - 0.0001:
            self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.y = concatenate((self.y[:1], self.y[:-1]), 1)
        self.y[0] = sin(self.phase) * (-1.0 + 2.0*random.random())
		
        # z moves from right to left:
        # Shift z array left and assign new value to z[n-1].
        self.z = concatenate((self.z[1:], self.z[:1]), 1)
        self.z[-1] = 0.8 - (2.0 * self.phase/pi) + 0.4*random.random()

        self.setCurveData(self.curveR, self.x, self.y)
        self.setCurveData(self.curveL, self.x, self.z)

        self.replot()
        self.phase += pi*0.02

    # timerEvent()

# class DataPlot

def main(args): 
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

def make():
    demo = DataPlot()
    demo.resize(500, 300)
    demo.show()
    return demo

# make()

# Admire
if __name__ == '__main__':
    main(sys.argv)
