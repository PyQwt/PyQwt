#!/usr/bin/env python

import sys
from qt import *
from qwt import *
from Numeric import *
import RandomArray

# MinPackDemo only works if SciPy is installed
import_error = None
try:
    from scipy.optimize.minpack import leastsq
except ImportError:
    import_error = ('scipy.optimize.minpack.leastsq',
                    'SciPy',
                    'http://www.scipy.org')

# the same function is used to make and to fit the data
# arguments are: the function parameters 'a', x-data and optional y-data
def function(a, x, y = 0):
    return a[0]/(1+(x/a[1])**2) + a[2]/(1+(x/a[3])**2) - y


class MinPackDemo(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)

	# make a QwtPlot widget
	self.plot = QwtPlot('A PyQwt and MinPack Demonstration', self)

	# initialize the noisy data
        scatter = 0.05
        x = arrayrange(-5.0, 5.0, 0.1)
        y = RandomArray.uniform(1.0-scatter, 1.0+scatter, shape(x)) * \
            function([1.0, 1.0, -2.0, 2.0], x)

        # fit from a reasonable initial guess
        guess = asarray([0.5, 1.5, -1.0, 3.0])
        yGuess = function(guess, x)
        solution = leastsq(function, guess, args=(x, y))
        yFit = function(solution[0], x)
        print solution

	# insert a few curves
	c1 = self.plot.insertCurve('data')
	c2 = self.plot.insertCurve('guess')
        c3 = self.plot.insertCurve('fit')
        
	# set curve styles
	self.plot.setCurvePen(c1, QPen(Qt.black))
        self.plot.setCurvePen(c2, QPen(Qt.red))
	self.plot.setCurvePen(c3, QPen(Qt.green))

	# copy the data
	self.plot.setCurveData(c1, x, y)
        self.plot.setCurveData(c2, x, yGuess)
        self.plot.setCurveData(c3, x, yFit)
	
	# set axis titles
	self.plot.setAxisTitle(QwtPlot.xBottom, 'x -->')
	self.plot.setAxisTitle(QwtPlot.yLeft, 'y -->')

        self.plot.enableLegend(1)
        self.plot.replot()
        	
    def resizeEvent(self, e):
    	self.plot.resize(e.size())
	self.plot.move(0,0)

# Admire!
app = QApplication(sys.argv)
if import_error: # Oops, but now we can create a message box
    mb = QMessageBox("MinPackDemo.py",
                     "MinPackDemo.py failed to import '%s'.\n"
                     "Install '%s' from <%s> and try again." % import_error,
                     QMessageBox.Critical,
                     QMessageBox.Ok | QMessageBox.Default,
                     QMessageBox.NoButton,
                     QMessageBox.NoButton)
    mb.exec_loop()
    raise SystemExit
demo = MinPackDemo()
app.setMainWidget(demo)
demo.show()
app.exec_loop()
