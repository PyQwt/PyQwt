#!/usr/bin/env python

import random, sys, time
from qt import *
from qwt import *
from Numeric import *

def standard_map(x_cor, y_cor, kappa):
    """provide one interate of the inital conditions x_cor,y_cor
       for the standard map with parameter kappa.
    """
    y_cor_new=y_cor-kappa*sin(2.0*pi*x_cor)
    x_cor_new=x_cor+y_cor_new

    # bring back to [0,1.0]^2
    if( (x_cor_new>1.0) or (x_cor_new<0.0) ): # you mean >1.0 or <0.0
         x_cor_new=x_cor_new-floor(x_cor_new)
    if( (y_cor_new>1.0) or (y_cor_new<0.0) ):
         y_cor_new=y_cor_new-floor(y_cor_new)

    return x_cor_new, y_cor_new


class MapDemo(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)

        self.plot = plot = QwtPlot(self);

        # Initialize map data
        self.n = 1 << 16 # 65536
        self.n = 1 << 10 #  1024
        self.xs = zeros(self.n, Float)
        self.ys = zeros(self.n, Float)
        self.i = self.n

        self.kappa = 0.2

        plot.setTitle("A Simple Map Demonstration")

        self.curve = plot.insertCurve("Map")

        plot.setCurveSymbol(self.curve, QwtSymbol(
            QwtSymbol.Ellipse, QBrush(Qt.red), QPen(Qt.blue), QSize(5, 5)))

        plot.setCurvePen(self.curve, QPen(Qt.cyan))

        plot.setAxisTitle(QwtPlot.xBottom, "x")
        plot.setAxisTitle(QwtPlot.yLeft, "y")
    
        # Set margins 
        plot.setAxisScale(QwtPlot.xBottom, 0.0, 1.0)
        plot.setAxisScale(QwtPlot.yLeft, 0.0, 1.0)

        # 1 tick = 1 ms, so plot new point every 0.05 sec
        self.ticks = 10
        self.tid = self.startTimer(self.ticks)
        self.phase = 0.0
        
    def resizeEvent(self, event):
        self.plot.resize(event.size())
        self.plot.move(0, 0)

    def moreData(self):
        if self.i == self.n:
            self.i = 0
            self.x = random.random()
            self.y = random.random()
            self.xs[self.i] = self.x
            self.ys[self.i] = self.y
            self.i += 1
            print self.x, self.y, time.time()
        else:
            self.x, self.y = standard_map(self.x, self.y, self.kappa)
            self.xs[self.i] = self.x
            self.ys[self.i] = self.y
            self.i += 1
        
    def timerEvent(self, e):
        self.moreData()
        self.plot.setCurveData(self.curve, self.xs[:self.i], self.ys[:self.i])
        self.plot.replot()
         

def main(args):
    app = QApplication(args)
    demo = MapDemo()
    demo.resize(600, 600)
    app.setMainWidget(demo)
    demo.show()
    app.exec_loop()


def make():
    demo = MapDemo()
    demo.resize(600, 600)
    demo.show()
    return demo

# Admire! 
if __name__ == '__main__':
    main(sys.argv)
