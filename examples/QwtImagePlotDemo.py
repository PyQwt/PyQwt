#!/usr/bin/env python

import sys
from qt import *
from qwt import *
from Numeric import *
import arrayfns

# from scipy.pilutil
def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if data.typecode == UInt8:
        return data
    high = high - low
    if cmin is None:
        cmin = min(ravel(data))
    if cmax is None:
        cmax = max(ravel(data))
    scale = high *1.0 / (cmax-cmin or 1)
    bytedata = ((data*1.0-cmin)*scale + 0.4999).astype(UInt8)
    return bytedata + asarray(low).astype(UInt8)

# bytescale()

def linearX(nx, ny):
    return repeat(arange(nx, typecode = Float32)[:, NewAxis], ny, -1)

# linearX()

def linearY(nx, ny):
    return repeat(arange(ny, typecode = Float32)[NewAxis, :], nx, 0)

# linearY()

def square(n, min, max):
    x = arrayfns.span(min, max, n, n)
    y = transpose(x)
    return sin(x)*cos(y)

# square()

def rectangle(nx, ny, scale):
    # swap axes in the fromfunction call
    s = scale/(nx+ny)
    x0 = nx/2
    y0 = ny/2
    
    def test(y, x):
        return cos(s*(x-x0))*sin(s*(y-y0))

    result = fromfunction(test, (ny, nx))
    return result

# rectangle()


class QwtPlotImage(QwtPlotMappedItem):

    def __init__(self, parent):
        QwtPlotItem.__init__(self, parent)
        self.xyzs = None
        self.plot = parent

    # __init__()
    
    def setData(self, xyzs, xScale = None, yScale = None):
        self.xyzs = xyzs
        shape = xyzs.shape
        if xScale:
            self.xMap = QwtDiMap(0, shape[0], xScale[0], xScale[1])
            self.plot.setAxisScale(QwtPlot.xBottom, *xScale)
        else:
            self.xMap = QwtDiMap(0, shape[0], 0, shape[0])
            self.plot.setAxisScale(QwtPlot.xBottom, 0, shape[0])
        if yScale:
            self.yMap = QwtDiMap(0, shape[1], yScale[0], yScale[1])
            self.plot.setAxisScale(QwtPlot.yLeft, *yScale)
        else:
            self.yMap = QwtDiMap(0, shape[1], 0, shape[1])
            self.plot.setAxisScale(QwtPlot.yLeft, 0, shape[1])
        self.image = toQImage(bytescale(self.xyzs)).mirror(0, 1)
        for i in range(0, 256):
            self.image.setColor(i, qRgb(i, 0, 255-i))

    # setData()    

    def drawImage(self, painter, xMap, yMap):
        """Paint image to zooming to xMap, yMap

        Calculate (x1, y1, x2, y2) so that it contains at least 1 pixel,
        and copy the visible region to scale it to the canvas.
        """
        # calculate y1, y2
        # the scanline order (index y) is inverted with respect to the y-axis
        y1 = y2 = self.image.height()
        y1 *= (self.yMap.d2() - yMap.d2())
        y1 /= (self.yMap.d2() - self.yMap.d1())
        y1 = max(0, int(y1-0.5))
        y2 *= (self.yMap.d2() - yMap.d1())
        y2 /= (self.yMap.d2() - self.yMap.d1())
        y2 = min(self.image.height(), int(y2+0.5))
        # calculate x1, x2 -- the pixel order (index x) is normal
        x1 = x2 = self.image.width()
        x1 *= (xMap.d1() - self.xMap.d1())
        x1 /= (self.xMap.d2() - self.xMap.d1())
        x1 = max(0, int(x1-0.5))
        x2 *= (xMap.d2() - self.xMap.d1())
        x2 /= (self.xMap.d2() - self.xMap.d1())
        x2 = min(self.image.width(), int(x2+0.5))
        # copy
        image = self.image.copy(x1, y1, x2-x1, y2-y1)
        # zoom
        image = image.smoothScale(xMap.i2()-xMap.i1()+1, yMap.i1()-yMap.i2()+1)
        # draw
        painter.drawImage(xMap.i1(), yMap.i2(), image)

    # drawImage()

# class QwtPlotImage
    

class QwtImagePlot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)
	# make a QwtPlot widget
        self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setAlignCanvasToScales(1)
	self.setTitle('QwtImagePlot: (un)zoom & (un)hide')
        self.setAutoLegend(1)
        self.setLegendPos(Qwt.Right)
	# set axis titles
	self.setAxisTitle(QwtPlot.xBottom, 'time (s)')
	self.setAxisTitle(QwtPlot.yLeft, 'frequency (Hz)')
	# insert a few curves
	cSin = self.insertCurve('y = pi*sin(x)')
	cCos = self.insertCurve('y = 4*pi*sin(x)*cos(x)**2')
	# set curve styles
	self.setCurvePen(cSin, QPen(Qt.green, 2))
	self.setCurvePen(cCos, QPen(Qt.black, 2))
	# calculate 3 NumPy arrays
        x = arrayrange(-2*pi, 2*pi, 0.01)
        y = pi*sin(x)
        z = 4*pi*cos(x)*cos(x)*sin(x)
	# copy the data
	self.setCurveData(cSin, x, y)
	self.setCurveData(cCos, x, z)
	# insert a horizontal marker at y = 0
	mY = self.insertLineMarker('y = 0', QwtPlot.yLeft)
	self.setMarkerYPos(mY, 0.0)
	# insert a vertical marker at x = pi
	mX = self.insertLineMarker('x = pi', QwtPlot.xBottom)
	self.setMarkerXPos(mX, pi)
        # image
        self.plotImage = QwtPlotImage(self)
        #self.plotImage.setData(bytescale(linearX(512, 512)+linearY(512, 512)))
        self.plotImage.setData(
            square(512,-2*pi, 2*pi), (-2*pi, 2*pi), (-2*pi, 2*pi))

        self.zoomStack = []
        self.connect(self,
                     SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)
        self.connect(self,
                     SIGNAL('plotMousePressed(const QMouseEvent&)'),
                     self.onMousePressed)
        self.connect(self,
                     SIGNAL('plotMouseReleased(const QMouseEvent&)'),
                     self.onMouseReleased)
        self.connect(self, SIGNAL("legendClicked(long)"), self.toggleCurve)
        
        # replot
        self.replot()

    # __init__()

    def drawCanvasItems(self, painter, rectangle, maps, filter):
        self.plotImage.drawImage(
            painter, maps[QwtPlot.xBottom], maps[QwtPlot.yLeft])
        QwtPlot.drawCanvasItems(self, painter, rectangle, maps, filter)

    # drawCanvasItems()

    def onMouseMoved(self, e):
        pass

    # onMouseMoved()

    def onMousePressed(self, e):
        if Qt.LeftButton == e.button():
            # Python semantics: self.pos = e.pos() does not work; force a copy
            self.xpos = e.pos().x()
            self.ypos = e.pos().y()
            self.enableOutline(1)
            self.setOutlinePen(QPen(Qt.black))
            self.setOutlineStyle(Qwt.Rect)
            self.zooming = 1
            if self.zoomStack == []:
                self.zoomState = (
                    self.axisScale(QwtPlot.xBottom).lBound(),
                    self.axisScale(QwtPlot.xBottom).hBound(),
                    self.axisScale(QwtPlot.yLeft).lBound(),
                    self.axisScale(QwtPlot.yLeft).hBound(),
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
            self.setOutlineStyle(Qwt.Cross)
            xmin = self.invTransform(QwtPlot.xBottom, xmin)
            xmax = self.invTransform(QwtPlot.xBottom, xmax)
            ymin = self.invTransform(QwtPlot.yLeft, ymin)
            ymax = self.invTransform(QwtPlot.yLeft, ymax)
            if xmin == xmax or ymin == ymax:
                return
            self.zoomStack.append(self.zoomState)
            self.zoomState = (xmin, xmax, ymin, ymax)
            self.enableOutline(0)
        elif Qt.RightButton == e.button():
            if len(self.zoomStack):
                xmin, xmax, ymin, ymax = self.zoomStack.pop()
            else:
                return

        self.setAxisScale(QwtPlot.xBottom, xmin, xmax)
        self.setAxisScale(QwtPlot.yLeft, ymin, ymax)
        self.replot()

    # onMouseReleased()

    def toggleCurve(self, key):
        curve = self.curve(key)
        if curve:
            curve.setEnabled(not curve.enabled())
            self.replot()

    # toggleCurve()

# class QwtImagePlot


def make():
    demo = QwtImagePlot()
    demo.resize(500, 300)
    demo.show()
    return demo

# make()

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

# Admire
if __name__ == '__main__':
    main(sys.argv)




