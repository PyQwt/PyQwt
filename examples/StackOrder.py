#!/usr/bin/env python

# Contributed by Tomaz Curk in a bug report showing that the stack order of the
# curves was dependent on the number of curves. This has been fixed in Qwt.
# Beautified by Gerard Vermeulen.

import sys
import math
from qt import *
from qwt import *

class BarQwtCurve(QwtPlotCurve):

    def __init__(self, parent, text):
        QwtPlotCurve.__init__(self, parent, text)
        self.color = Qt.black

    # __init__()
    
    def draw(self, p, xMap, yMap, f, t):
        p.setBackgroundMode(Qt.TransparentMode)
        p.setBackgroundColor(self.color)
        p.setBrush(self.color)
        p.setPen(QPen(Qt.red, 2))
        if t < 0:
            t = self.dataSize() - 1
        if divmod(f, 2)[1] != 0:
            f -= 1
        if divmod(t, 2)[1] == 0:
            t += 1
        for i in range(f, t+1, 2):
            px1 = xMap.transform(self.x(i))
            py1 = yMap.transform(self.y(i))
            px2 = xMap.transform(self.x(i+1))
            py2 = yMap.transform(self.y(i+1))
            p.drawRect(px1, py1, (px2 - px1), (py2 - py1))

    # draw()

# class BarQwtCurve

class StackOrderDemo(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.graph = QwtPlot("Check the stack order of the bars: "
                             "leftclick and drag to zoom, "
                             "rightclick to unzoom.", self)
        self.setCentralWidget(self.graph)

        # The mouse
        self.graph.canvas().setMouseTracking(1)
        self.statusBar().message("Move the cursor with the plot"
                                 " to show the cursor position")
        self.zoomStack = []
        self.connect(self.graph,
                     SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)
        self.connect(self.graph,
                     SIGNAL('plotMousePressed(const QMouseEvent&)'),
                     self.onMousePressed)
        self.connect(self.graph,
                     SIGNAL('plotMouseReleased(const QMouseEvent&)'),
                     self.onMouseReleased)

        # The number of bars -- the widget gets slow for more than 1000 bars
        self.toolBar = QToolBar(self)
        self.toolBar.setStretchableWidget(QWidget(self.toolBar))
        counterBox = QHBox(self.toolBar)
        counterBox.setSpacing(10)
        QLabel("Number of bars", counterBox)
        self.counter = QwtCounter(counterBox)
        self.counter.setRange(0, 10000, 1)
        self.counter.setValue(0)
        self.counter.setNumButtons(3)
        self.connect(self.counter, SIGNAL('valueChanged(double)'), self.plot)
        self.graph.replot()

    # __init__()
    
    def plot(self, x):
        """Create and plot a sequence of int(x) curves (bars)"""
        self.graph.removeCurves()

        for i in range(int(x)):
            curve = BarQwtCurve(self.graph, str(100+i))
            curve.color = Qt.blue
            ckey = self.graph.insertCurve(curve)
            self.graph.setCurveStyle(ckey, QwtCurve.UserCurve)
            self.graph.setCurveData(ckey, [i, i+1.4], [0.3*i, 5.0+0.3*i])

        self.graph.replot()

    def onMouseMoved(self, e):
        self.statusBar().message(
            "x = %+.6g, y = %.6g"
            % (self.graph.invTransform(QwtPlot.xBottom, e.pos().x()),
               self.graph.invTransform(QwtPlot.yLeft, e.pos().y())))

    # onMouseMoved()
    
    def onMousePressed(self, e):
        if Qt.LeftButton == e.button():
            # Python semantics: self.pos = e.pos() does not work; force a copy
            self.xpos = e.pos().x()
            self.ypos = e.pos().y()
            self.graph.enableOutline(1)
            self.graph.setOutlinePen(QPen(Qt.black))
            self.graph.setOutlineStyle(Qwt.Rect)
            self.zooming = 1
            if self.zoomStack == []:
                self.zoomState = (
                    self.graph.axisScale(QwtPlot.xBottom).lBound(),
                    self.graph.axisScale(QwtPlot.xBottom).hBound(),
                    self.graph.axisScale(QwtPlot.yLeft).lBound(),
                    self.graph.axisScale(QwtPlot.yLeft).hBound(),
                    )
        elif Qt.RightButton == e.button():
            self.zooming = 0
        # fake a mouse move to show the cursor position
        self.onMouseMoved(e)

    # onMousePressed()

    def onMouseReleased(self, e):
        if Qt.LeftButton == e.button():
            xmin = min(self.xpos, e.pos().x())
            xmax = max(self.xpos, e.pos().x())
            ymin = min(self.ypos, e.pos().y())
            ymax = max(self.ypos, e.pos().y())
            self.graph.setOutlineStyle(Qwt.Cross)
            xmin = self.graph.invTransform(QwtPlot.xBottom, xmin)
            xmax = self.graph.invTransform(QwtPlot.xBottom, xmax)
            ymin = self.graph.invTransform(QwtPlot.yLeft, ymin)
            ymax = self.graph.invTransform(QwtPlot.yLeft, ymax)
            if xmin == xmax or ymin == ymax:
                return
            self.zoomStack.append(self.zoomState)
            self.zoomState = (xmin, xmax, ymin, ymax)
            self.graph.enableOutline(0)
        elif Qt.RightButton == e.button():
            if len(self.zoomStack):
                xmin, xmax, ymin, ymax = self.zoomStack.pop()
            else:
                return

        self.graph.setAxisScale(QwtPlot.xBottom, xmin, xmax)
        self.graph.setAxisScale(QwtPlot.yLeft, ymin, ymax)
        self.graph.replot()

    # onMouseReleased()

# class StackOrderDemo

# Admire
a = QApplication(sys.argv)
w = StackOrderDemo()
a.setMainWidget(w)
w.resize(800, 600)
w.show()
a.exec_loop()

