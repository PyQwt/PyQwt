#!/usr/bin/env python

# The Python version of qwt-*/examples/data_plot/data_plot.cpp
# Example finished by Andreas Gerber.

import random, sys
from qt import *
from qwt import *
from Numeric import *


class DataDemo(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)

        self.plot = plot = QwtPlot(self);

        # Initialize data
        self.x1 = arrayrange(0.0, 100.1, 0.5)
        self.x2 = arrayrange(0.0, 300.3, 1.5)
        self.y = zeros(len(self.x1), Float)
        self.z = zeros(len(self.x1), Float)

        plot.setTitle("Another Simple QwtPlot Demonstration")

        self.curveR = plot.insertCurve("Data Moving Right")
        self.curveL = plot.insertCurve("Data Moving Left")

        plot.setCurveSymbol(self.curveL, QwtSymbol(
            QwtSymbol.Ellipse, QBrush(), QPen(Qt.yellow), QSize(7, 7)))

        plot.setCurvePen(self.curveR, QPen(Qt.red))
        plot.setCurvePen(self.curveL, QPen(Qt.blue))

        mY = plot.insertLineMarker("", QwtPlot.yLeft)      
        plot.setMarkerYPos(mY, 0.0)

        plot.setAxisTitle(QwtPlot.xBottom, "Time (seconds)")
        plot.setAxisTitle(QwtPlot.yLeft, "Values")
    
        # Set margins 
        plot.setAxisScale(QwtPlot.xBottom, 0.0, 100.0)

        # Display a legend
        plot.enableLegend(1);

        self.tid = self.startTimer(50);
        self.phase = 0.0
        
    def resizeEvent(self, event):
        self.plot.resize(event.size())
        self.plot.move(0, 0)

    def newData(self):
        if self.phase > pi - 0.0001: self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.y = concatenate((self.y[:1], self.y[:-1]),1)
        self.y[0] = sin(self.phase) * (-1.0 +2.0*random.random())
		
        # z moves from right to left:
        # Shift z array left and assign new value to z[n-1].
        self.z = concatenate((self.z[1:], self.z[:1]), 1)
        self.z[-1] = 0.8 - (2.0 * self.phase/pi) +0.4*random.random()

        self.phase += pi*0.02

    def timerEvent(self, e):
        self.newData()
        self.plot.setCurveData(self.curveR, self.x1, self.y)
        self.plot.setCurveData(self.curveL, self.x2, self.z)

        self.plot.replot()

         
def main(args): 
    app = QApplication(args)
    demo = DataDemo()
    app.setMainWidget(demo)
    demo.show()
    app.exec_loop()


def make():
    demo = DataDemo()
    demo.show()
    return demo


# Admire
if __name__ == '__main__':
    main(sys.argv)
