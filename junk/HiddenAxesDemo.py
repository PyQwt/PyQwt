#!/usr/bin/env python

# The Python version of qwt-*/examples/simple_plot/simple.cpp

import sys
from qt import *
from qwt import *
from Numeric import *

class HiddenScaleDraw(QwtScaleDraw):
    def __init__(self, *args):
        QwtScaleDraw.__init__(self, *args)
        
    def label(self, value):
        return QString.null

class HiddenAxesPlot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)
	# make a QwtPlot widget
	self.setTitle('Hiding the axes without loosing the scales')
        self.setAutoLegend(0)
        self.setLegendPos(Qwt.Right)
        self.setAxisScaleDraw(QwtPlot.xBottom, HiddenScaleDraw())
        self.setAxisScaleDraw(QwtPlot.yLeft, HiddenScaleDraw())

        self.setAxisScale(QwtPlot.yLeft, -2.0, 2.0)
        scaleDraw = self.axisScaleDraw(QwtPlot.xBottom)
        scaleDraw.setOptions(0)
        scaleDraw.setTickLength(0, 0, 1)
        self.setAxisScaleDraw(QwtPlot.xBottom, scaleDraw)
        self.setAxisScale(QwtPlot.xBottom, 0.0, 20.0)
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
	

# admire	
app = QApplication(sys.argv)
demo = HiddenAxesPlot()
app.setMainWidget(demo)
demo.resize(500, 300)
demo.show()
app.exec_loop()




