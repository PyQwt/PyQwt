#!/usr/bin/env python

# Plot of Numeric & numarray arrays and lists & tuples of Python floats.

import sys
from qt import *
from qwt import *

def drange(start, stop, step):
    start, stop, step = float(start), float(stop), float(step)
    size = int(round((stop-start)/step))
    result = [start]*size
    for i in xrange(size):
        result[i] += i*step
    return result
        
def lorentzian(x):
    return 1.0/(1.0+(x-5.0)**2)


class MultiDemo(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)

        grid = QGridLayout(self, 2, 2);
        
        # try to create a plot widget for Numeric arrays
        try:
            import Numeric
            # import does_not_exist
            numeric_plot = QwtPlot('Plot -- Numeric arrays', self)
            numeric_plot.plotLayout().setCanvasMargin(0)
            numeric_plot.plotLayout().setAlignCanvasToTicks(1)
            numeric_x = Numeric.arange(0.0, 10.0, 0.01)
            numeric_y = lorentzian(numeric_x)
            # insert a curve, make it red and copy the arrays
            key = numeric_plot.insertCurve('y = lorentzian(x)')
            numeric_plot.setCurvePen(key, QPen(Qt.red))
            numeric_plot.setCurveData(key, numeric_x, numeric_y)
            grid.addWidget(numeric_plot, 0, 0)
            numeric_plot.replot()
        except ImportError, message:
            print "%s: %s" % (ImportError, message)
            print "Cannot show how to plot Numeric arrays"

        # create a plot widget for lists of Python floats
        list_plot = QwtPlot('Plot -- List of Python floats', self)
        list_plot.plotLayout().setCanvasMargin(0)
        list_plot.plotLayout().setAlignCanvasToTicks(1)
        list_x = drange(0.0, 10.0, 0.01)
        list_y = map(lorentzian, list_x)
        # insert a curve, make it blue and copy the lists
        key = list_plot.insertCurve('y = lorentzian(x)')
        list_plot.setCurvePen(key, QPen(Qt.blue))
        list_plot.setCurveData(key, list_x, list_y)
        grid.addWidget(list_plot, 1, 0)
        list_plot.replot()

        # create a plot widget for tuples of Python floats
        tuple_plot = QwtPlot('Plot -- Tuple of Python floats', self)
        tuple_plot.plotLayout().setCanvasMargin(0)
        tuple_plot.plotLayout().setAlignCanvasToTicks(1)
        tuple_x = tuple(list_x)
        tuple_y = tuple(list_y)
        # insert a curve, make it blue and copy the lists
        key = tuple_plot.insertCurve('y = lorentzian(x)')
        tuple_plot.setCurvePen(key, QPen(Qt.blue))
        tuple_plot.setCurveData(key, tuple_x, tuple_y)
        grid.addWidget(tuple_plot, 0, 1)
        tuple_plot.replot()

        # try to create a plot widget for numarray arrays
        try:
            import numarray
            # import does_not_exist
            numarray_plot = QwtPlot('Plot -- numarray arrays', self)
            numarray_plot.plotLayout().setCanvasMargin(0)
            numarray_plot.plotLayout().setAlignCanvasToTicks(1)
            numarray_x = numarray.arange(0.0, 10.0, 0.01)
            numarray_y = lorentzian(numarray_x)
            # insert a curve, make it red and copy the arrays
            key = numarray_plot.insertCurve('y = lorentzian(x)')
            numarray_plot.setCurvePen(key, QPen(Qt.red))
            numarray_plot.setCurveData(key, numarray_x, numarray_y)
            grid.addWidget(numarray_plot, 1, 1)
            numarray_plot.replot()
        except ImportError, message:
            print "%s: %s" % (ImportError, message)
            print "Cannot show how to plot numarray arrays"
            pass

    # __init__()

# class MultiDemo


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()


def make():
    demo = MultiDemo()
    demo.resize(400, 600)
    demo.show()
    return demo

# Admire!
if __name__ == '__main__':
    main(sys.argv)

        

