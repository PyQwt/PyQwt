#!/usr/bin/env python

# The Python version of qwt-*/examples/simple_plot/simple.cpp

import sys
from qt import *
from qwt import *
from Numeric import *

class SimplePlot(QwtPlot):

    def __init__(self, *args):
        apply(QwtPlot.__init__, (self,) + args)
	# make a QwtPlot widget
	self.setTitle('A Simple PyQwt Plot Demonstration')
        self.setAutoLegend(1)
        self.setLegendPosition(QwtPlot.Right)
	# set axis titles
	self.setAxisTitle(QwtPlot.xBottom, 'x -->')
	self.setAxisTitle(QwtPlot.yLeft, 'y -->')
	# insert a few curves
	cSin = self.insertCurve('y = sin(x)')
	cCos = self.insertCurve('y = cos(x)')
	# set curve styles
	self.setCurvePen(cSin, QPen(Qt.red))
	self.setCurvePen(cCos, QPen(Qt.blue))
	# calculate 3 NumPy arrays
        x = arrayrange(0.0, 10.0, 0.1)
        y = sin(x)
        z = cos(x)
	# copy the data
	self.setCurveData(cSin, x, y)
	self.setCurveData(cCos, x, z)
	# insert a horizontal marker at y = 0
	mY = self.insertLineMarker('y = 0', QwtPlot.yLeft)
	self.setMarkerYPos(mY, 0.0)
	# insert a vertical marker at x = 2 pi
	mX = self.insertLineMarker('x = 2 pi', QwtPlot.xBottom)
	self.setMarkerXPos(mX, 2*pi)
        # replot
        self.replot()
	

def make():
    demo = SimplePlot()
    demo.resize(500, 300)
    demo.show()
    return demo

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()


# Admire
if __name__ == '__main__':
    main(sys.argv)




