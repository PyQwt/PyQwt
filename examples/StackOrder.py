#!/usr/bin/env python

# Contributed by Tomaz Curk in a bug report showing that the stack order of the
# curves was dependent on the number of curves. This has been fixed in Qwt.
#
# QwtBarCurve is an idea of Tomaz Curk.
#
# Beautified and expanded by Gerard Vermeulen.

import math
import random
import sys
from qt import *
from qwt import *

class QwtBarCurve(QwtPlotCurve):

    def __init__(self, parent, penColor=Qt.black, brushColor=Qt.white):
        QwtPlotCurve.__init__(self, parent)
        self.penColor = penColor
        self.brushColor = brushColor
        
    # __init__()
    
    def draw(self, painter, xMap, yMap, start, stop):
        """Draws rectangles with the corners taken from the x- and y-arrays.
        """
        if type(self.penColor) == type(Qt.black):
            painter.setPen(QPen(self.penColor, 2))
        else:
            painter.setPen(QPen(Qt.NoPen))
        if type(self.brushColor) == type(Qt.white):
            painter.setBrush(self.brushColor)
        if stop == -1:
            stop = self.dataSize()
        # force 'start' and 'stop' to be even and positive
        if start & 1:
            start -= 1
        if stop & 1:
            stop -= 1
        start = max(start, 0)
        stop = max(stop, 0)
        for i in range(start, stop, 2):
            px1 = xMap.transform(self.x(i))
            py1 = yMap.transform(self.y(i))
            px2 = xMap.transform(self.x(i+1))
            py2 = yMap.transform(self.y(i+1))
            painter.drawRect(px1, py1, (px2 - px1), (py2 - py1))

    # draw()

# class QwtBarCurve


class QwtBarPlotDemo(QMainWindow):

    table = {
        'none': None,
        'black': Qt.black,
        'blue': Qt.blue,
        'cyan': Qt.cyan,
        'gray': Qt.gray,
        'green': Qt.green,
        'magenta': Qt.magenta,
        'red': Qt.red,
        'white': Qt.white,
        'yellow': Qt.yellow,
        }
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Initialize a QwPlot central widget
        self.plot = QwtPlot('left-click & drag to zoom'
                            ' -- '
                            'right-click to unzoom',
                            self)
        self.plot.plotLayout().setCanvasMargin(0)
        self.plot.plotLayout().setAlignCanvasToScales(True)
        self.setCentralWidget(self.plot)

        self.__initToolBar()
        self.__initTracking()
        self.__initZooming()
        
        # Finalize
        self.counter.setValue(10)
        self.go(self.counter.value())

    # __init__()

    def __initToolBar(self):
        """Initialize the toolbar
        """
        
        self.toolBar = QToolBar(self)

        QLabel("Pen:", self.toolBar)

        self.penComboBox = QComboBox(self.toolBar)
        for name in self.table.keys():
            self.penComboBox.insertItem(name)
        self.penComboBox.setCurrentItem(
            random.randint(0, self.penComboBox.count()-1))

        QLabel("Brush:", self.toolBar)

        self.brushComboBox = QComboBox(self.toolBar)
        for name in self.table.keys():
            self.brushComboBox.insertItem(name)
        self.brushComboBox.setCurrentItem(
            random.randint(0, self.brushComboBox.count()-1))

        self.toolBar.setStretchableWidget(QWidget(self.toolBar))

        QLabel("Bars:", self.toolBar)

        self.counter = QwtCounter(self.toolBar)
        self.counter.setRange(0, 10000, 1)
        self.counter.setNumButtons(3)

        self.connect(self.counter, SIGNAL('valueChanged(double)'), self.go)
        self.connect(self.penComboBox, SIGNAL('activated(int)'), self.go)
        self.connect(self.brushComboBox, SIGNAL('activated(int)'), self.go)

    # __initToolBar()

    def __initTracking(self):
        """Initialize tracking
        """
        
        self.plot.canvas().setMouseTracking(True)
        self.statusBar().message(
            "Plot cursor movements are tracked in the status bar")

    # __initTracking()

    def __initZooming(self):
        """Initialize zooming
        """

        self.zoomStack = []
        self.connect(self.plot,
                     SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)
        self.connect(self.plot,
                     SIGNAL('plotMousePressed(const QMouseEvent&)'),
                     self.onMousePressed)
        self.connect(self.plot,
                     SIGNAL('plotMouseReleased(const QMouseEvent&)'),
                     self.onMouseReleased)

    # __initZooming()
       
    def go(self, x):
        """Create and plot a sequence bars taking into account the controls
        """

        if type(x) == type(0):
            # activated(int)
            x = int(self.counter.value())
        else:
            # valueChanged(double)
            self.clearZoomStack()

        penColor = self.table[str(self.penComboBox.currentText())]
        brushColor = self.table[str(self.brushComboBox.currentText())]
            
        self.plot.removeCurves()

        for i in range(x):
            curve = QwtBarCurve(self.plot, penColor, brushColor)
            key = self.plot.insertCurve(curve)
            self.plot.setCurveStyle(key, QwtCurve.UserCurve)
            self.plot.setCurveData(key, [i, i+1.4], [0.3*i, 5.0+0.3*i])

        self.plot.replot()

    # go()

    def onMouseMoved(self, e):
        self.statusBar().message(
            "x = %+.6g, y = %.6g"
            % (self.plot.invTransform(QwtPlot.xBottom, e.pos().x()),
               self.plot.invTransform(QwtPlot.yLeft, e.pos().y())))

    # onMouseMoved()
    
    def clearZoomStack(self):
        for i in (QwtPlot.xBottom, QwtPlot.yLeft):
            self.plot.setAxisAutoScale(i)
        self.zoomStack = []

    # clearZoomStack()
    
    def onMousePressed(self, e):
        if Qt.LeftButton == e.button():
            # Python semantics: self.pos = e.pos() does not work; force a copy
            self.xpos = e.pos().x()
            self.ypos = e.pos().y()
            self.plot.enableOutline(1)
            self.plot.setOutlinePen(QPen(Qt.black))
            self.plot.setOutlineStyle(Qwt.Rect)
            self.zooming = 1
            if self.zoomStack == []:
                self.zoomState = (
                    self.plot.axisScale(QwtPlot.xBottom).lBound(),
                    self.plot.axisScale(QwtPlot.xBottom).hBound(),
                    self.plot.axisScale(QwtPlot.yLeft).lBound(),
                    self.plot.axisScale(QwtPlot.yLeft).hBound(),
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
            self.plot.setOutlineStyle(Qwt.Cross)
            xmin = self.plot.invTransform(QwtPlot.xBottom, xmin)
            xmax = self.plot.invTransform(QwtPlot.xBottom, xmax)
            ymin = self.plot.invTransform(QwtPlot.yLeft, ymin)
            ymax = self.plot.invTransform(QwtPlot.yLeft, ymax)
            if xmin == xmax or ymin == ymax:
                return
            self.zoomStack.append(self.zoomState)
            self.zoomState = (xmin, xmax, ymin, ymax)
            self.plot.enableOutline(0)
        elif Qt.RightButton == e.button():
            if len(self.zoomStack):
                xmin, xmax, ymin, ymax = self.zoomStack.pop()
            else:
                return

        self.plot.setAxisScale(QwtPlot.xBottom, xmin, xmax)
        self.plot.setAxisScale(QwtPlot.yLeft, ymin, ymax)
        self.plot.replot()

    # onMouseReleased()

# class StackOrderDemo


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

def make():
    demo = QwtBarPlotDemo()
    demo.resize(500, 500)
    demo.show()
    return demo

# make()

# Admire!
if __name__ == '__main__':
    main(sys.argv)

