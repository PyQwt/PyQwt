#!/usr/bin/env python

import sys
from qt import *
from qwt import *

# try to import scipy, Numeric, or numarray
try:
    from scipy import *
except ImportError:
    try:
        from Numeric import *
    except ImportError:
        try:
            from numarray import *
        except ImportError:
            raise ImportError, 'Failed to import scipy, Numeric, or numarray'


class ErrorBarPlotCurve(QwtPlotCurve):

    def __init__(self, parent,
                 x = [], y = [], dx = None, dy = None,
                 curvePen = QPen(Qt.NoPen),
                 curveStyle = QwtCurve.Lines,
                 curveSymbol = QwtSymbol(),
                 errorPen = QPen(Qt.NoPen),
                 errorCap = 0,
                 errorOnTop = False,
                 ):
        """A curve of x versus y data with error bars in dx and dy.

        Horizontal error bars are plotted if dx is not None.
        Vertical error bars are plotted if dy is not None.

        x and y must be sequences with a shape (N,) and dx and dy must be
        sequences (if not None) with a shape (), (N,), or (2, N):
        - if dx or dy has a shape () or (N,), the error bars are given by
          (x-dx, x+dx) or (y-dy, y+dy),
        - if dx or dy has a shape (2, N), the error bars are given by
          (x-dx[0], x+dx[1]) or (y-dy[0], y+dy[1]).

        curvePen is the pen used to plot the curve
        
        curveStyle is the style used to plot the curve
        
        curveSymbol is the symbol used to plot the symbols
        
        errorPen is the pen used to plot the error bars
        
        errorCap is the size of the error bar caps
        
        errorOnTop is a boolean:
        - if True, plot the error bars on top of the curve,
        - if False, plot the curve on top of the error bars.
        """

        QwtPlotCurve.__init__(self, parent)
        self.setData(x, y, dx, dy)
        self.setPen(curvePen)
        self.setStyle(curveStyle)
        self.setSymbol(curveSymbol)
        self.errorPen = errorPen
        self.errorCap = errorCap
        self.errorOnTop = errorOnTop

    # __init__()

    def setData(self, x, y, dx = None, dy = None):
        """Set x versus y data with error bars in dx and dy.

        Horizontal error bars are plotted if dx is not None.
        Vertical error bars are plotted if dy is not None.

        x and y must be sequences with a shape (N,) and dx and dy must be
        sequences (if not None) with a shape (), (N,), or (2, N):
        - if dx or dy has a shape () or (N,), the error bars are given by
          (x-dx, x+dx) or (y-dy, y+dy),
        - if dx or dy has a shape (2, N), the error bars are given by
          (x-dx[0], x+dx[1]) or (y-dy[0], y+dy[1]).
        """
        
        self.__x = asarray(x, Float)
        if len(self.__x.shape) != 1:
            raise RuntimeError, 'len(asarray(x).shape) != 1'

        self.__y = asarray(y, Float)
        if len(self.__y.shape) != 1:
            raise RuntimeError, 'len(asarray(y).shape) != 1'
        if len(self.__x) != len(self.__y):
            raise RuntimeError, 'len(asarray(x)) != len(asarray(y))' 

        if dx is None:
            self.__dx = None
        else:
            self.__dx = asarray(dx, Float)
        if len(self.__dx.shape) not in [0, 1, 2]:
            raise RuntimeError, 'len(asarray(dx).shape) not in [0, 1, 2]'
            
        if dy is None:
            self.__dy = dy
        else:
            self.__dy = asarray(dy, Float)
        if len(self.__dy.shape) not in [0, 1, 2]:
            raise RuntimeError, 'len(asarray(dy).shape) not in [0, 1, 2]'
        
        QwtPlotCurve.setData(self, self.__x, self.__y)

    # setData()
        
    def boundingRect(self):
        """Return the bounding rectangle of the data, error bars included.
        """
        if self.__dx is None:
            xmin = min(self.__x)
            xmax = max(self.__x)
        elif len(self.__dx.shape) in [0, 1]:
            xmin = min(self.__x - self.__dx)
            xmax = max(self.__x + self.__dx)
        else:
            xmin = min(self.__x - self.__dx[0])
            xmax = max(self.__x + self.__dx[1])

        if self.__dy is None:
            ymin = min(self.__y)
            ymax = max(self.__y)
        elif len(self.__dy.shape) in [0, 1]:
            ymin = min(self.__y - self.__dy)
            ymax = max(self.__y + self.__dy)
        else:
            ymin = min(self.__y - self.__dy[0])
            ymax = max(self.__y + self.__dy[1])

        return QwtDoubleRect(xmin, xmax, ymin, ymax)
        
    # boundingRect()

    def draw(self, painter, xMap, yMap, first, last = -1):
        """Draw an interval of the curve, including the error bars

        painter is the QPainter used to draw the curve

        xMap is the QwtDiMap used to map x-values to pixels

        yMap is the QwtDiMap used to map y-values to pixels
        
        first is the index of the first data point to draw

        last is the index of the last data point to draw. If last < 0, last
        is transformed to index the last data point
        """
        
        if last < 0:
            last = self.dataSize() - 1
        if not self.verifyRange(first, last):
            return

        if self.errorOnTop:
            QwtPlotCurve.draw(self, painter, xMap, yMap, first, last)

        # draw the error bars
        painter.save()
        painter.setPen(self.errorPen)

        # draw the error bars with caps in the x direction
        if self.__dx is not None:
            # draw the bars
            if len(self.__dx.shape) in [0, 1]:
                xmin = (self.__x - self.__dx)[first:last+1]
                xmax = (self.__x + self.__dx)[first:last+1]
            else:
                xmin = (self.__x - self.__dx[0])[first:last+1]
                xmax = (self.__x + self.__dx[1])[first:last+1]
            y = self.__y[first:last+1]
            n, i, j = len(y), 0, 0
            lines = QPointArray(2*n)
            while i < n:
                yi = yMap.transform(y[i])
                lines.setPoint(j, xMap.transform(xmin[i]), yi)
                j += 1
                lines.setPoint(j, xMap.transform(xmax[i]), yi)
                j += 1; i += 1
            painter.drawLineSegments(lines)
            if self.errorCap > 0:
                # draw the caps
                cap = self.errorCap/2
                n, i, j = len(y), 0, 0
                lines = QPointArray(4*n)
                while i < n:
                    yi = yMap.transform(y[i])
                    lines.setPoint(j, xMap.transform(xmin[i]), yi - cap)
                    j += 1
                    lines.setPoint(j, xMap.transform(xmin[i]), yi + cap)
                    j += 1
                    lines.setPoint(j, xMap.transform(xmax[i]), yi - cap)
                    j += 1
                    lines.setPoint(j, xMap.transform(xmax[i]), yi + cap)
                    j += 1; i += 1
            painter.drawLineSegments(lines)

        # draw the error bars with caps in the y direction
        if self.__dy is not None:
            # draw the bars
            if len(self.__dy.shape) in [0, 1]:
                ymin = (self.__y - self.__dy)[first:last+1]
                ymax = (self.__y + self.__dy)[first:last+1]
            else:
                ymin = (self.__y - self.__dy[0])[first:last+1]
                ymax = (self.__y + self.__dy[1])[first:last+1]
            x = self.__x[first:last+1]
            n, i, j = len(x), 0, 0
            lines = QPointArray(2*n)
            while i < n:
                xi = xMap.transform(x[i])
                lines.setPoint(j, xi, yMap.transform(ymin[i]))
                j += 1
                lines.setPoint(j, xi, yMap.transform(ymax[i]))
                j += 1; i += 1
            painter.drawLineSegments(lines)
            # draw the caps
            if self.errorCap > 0:
                cap = self.errorCap/2
                n, i, j = len(x), 0, 0
                lines = QPointArray(4*n)
                while i < n:
                    xi = xMap.transform(x[i])
                    lines.setPoint(j, xi - cap, yMap.transform(ymin[i]))
                    j += 1
                    lines.setPoint(j, xi + cap, yMap.transform(ymin[i]))
                    j += 1
                    lines.setPoint(j, xi - cap, yMap.transform(ymax[i]))
                    j += 1
                    lines.setPoint(j, xi + cap, yMap.transform(ymax[i]))
                    j += 1; i += 1
            painter.drawLineSegments(lines)

        painter.restore()

        if not self.errorOnTop:
            QwtPlotCurve.draw(self, painter, xMap, yMap, first, last)

    # draw()

# class ErrorBarPlotCurve


def make():
    # create a plot with a white canvas
    demo = QwtPlot("Errorbar Demonstation")
    demo.setCanvasBackground(Qt.white)
    # calculate data and errors for a curve with error bars
    x = arange(0, 10.1, 0.5, Float)
    y = sin(x)
    dy = 0.2 * abs(y)
    # dy = (0.15 * abs(y), 0.25 * abs(y)) # uncomment for asymmetric error bars
    dx = 0.2 # all error bars the same size
    errorOnTop = False # uncomment to draw the curve on top of the error bars
    # errorOnTop = True # uncomment to draw the error bars on top of the curve
    curve = ErrorBarPlotCurve(
        demo,
        x = x,
        y = y,
        dx = dx,
        dy = dy,
        curvePen = QPen(Qt.black, 2),
        curveStyle = QwtCurve.Spline,
        curveSymbol = QwtSymbol(QwtSymbol.Ellipse,
                                QBrush(Qt.red),
                                QPen(Qt.black, 2),
                                QSize(9, 9)),
        errorPen = QPen(Qt.blue, 2),
        errorCap = 10,
        errorOnTop = errorOnTop,
        )
    demo.insertCurve(curve)
    demo.resize(600, 400)
    demo.replot()
    demo.show()
    return demo

# make()


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    zoomer = QwtPlotZoomer(QwtPlot.xBottom,
                           QwtPlot.yLeft,
                           QwtPicker.DragSelection,
                           QwtPicker.AlwaysOff,
                           demo.canvas())
    zoomer.setRubberBandPen(QPen(Qt.green))
    picker = QwtPlotPicker(QwtPlot.xBottom,
                           QwtPlot.yLeft,
                           QwtPicker.NoSelection,
                           QwtPlotPicker.CrossRubberBand,
                           QwtPicker.AlwaysOn,
                           demo.canvas())
    picker.setRubberBandPen(QPen(Qt.green))
    picker.setCursorLabelPen(QPen(Qt.black))
    app.exec_loop()

# main()


# Admire!
if __name__ == '__main__':
    main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***
