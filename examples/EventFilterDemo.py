#!/usr/bin/env python

# The Python version of qwt-*/examples/event_filter

import sys
from qt import *
from qwt import *
from Numeric import *

class ColorBar(QWidget):
    def __init__(self, orientation, *args):
        QWidget.__init__(self, *args)
        self.__orientation = orientation
        self.__light = Qt.white
        self.__dark = Qt.black
        self.setCursor(Qt.pointingHandCursor)

    def setOrientation(self, orientation):
        self.__orientation = orientation
        self.update()

    def orientation(self):
        return self.__orientation

    def setRange(self, light, dark):
        self.__light = light
        self.__dark = dark
        self.update()

    def setLight(self, color):
        self.__light = color
        self.update()

    def setDark(self, color):
        self.__dark = color
        self.update()

    def light(self):
        return self.__light

    def dark(self):
        return self.__dark

    def mousePressEvent(self, event):
        if event.button() ==  Qt.LeftButton:
            pm = QPixmap.grabWidget(self)
            color = QColor()
            color.setRgb(pm.convertToImage().pixel(event.x(), event.y()))
            self.emit(PYSIGNAL("colorSelected"), (color,))
        if qVersion() >= '3.0.0':
            event.accept()

    def paintEvent(self, _):
        painter = QPainter(self)
        self.drawColorBar(painter, self.rect())

    def drawColorBar(self, painter, rect):
        h1, s1, v1 = self.__light.getHsv()
        h2, s2, v2 = self.__dark.getHsv()
        painter.save()
        painter.setClipRect(rect)
        painter.setClipping(True)
        painter.fillRect(rect, QBrush(self.__dark))
        sectionSize = 2
        if (self.__orientation == Qt.Horizontal):
            numIntervalls = rect.width()/sectionSize
        else:
            numIntervalls = rect.height()/sectionSize
        section = QRect()
        for i in range(numIntervalls):
            if self.__orientation == Qt.Horizontal:
                section.setRect(rect.x() + i*sectionSize, rect.y(),
                                sectionSize, rect.heigh())
            else:
                section.setRect(rect.x(), rect.y() + i*sectionSize,
                                rect.width(), sectionSize)
            ratio = float(i)/float(numIntervalls)
            painter.fillRect(section,
                             QBrush(QColor(h1 + int(ratio*(h2-h1) + 0.5),
                                           s1 + int(ratio*(s2-s1) + 0.5),
                                           v1 + int(ratio*(v2-v1) + 0.5),
                                           QColor.Hsv)))
        painter.restore()


class Plot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        self.setTitle("Interactive Plot")
        self.setCanvasColor(Qt.darkCyan)
        self.setGridMajPen(QPen(Qt.white, 0, Qt.DotLine))
        self.setAxisScale(QwtPlot.xBottom, 0.0, 100.0)
        self.setAxisScale(QwtPlot.yLeft, 0.0, 100.0)

        self.plotLayout().setAlignCanvasToScales(True)

        self.__insertCurve(Qt.Vertical, Qt.blue, 30.0)
        self.__insertCurve(Qt.Vertical, Qt.magenta, 70.0)
        self.__insertCurve(Qt.Horizontal, Qt.yellow, 30.0)
        self.__insertCurve(Qt.Horizontal, Qt.white, 70.0)
        
        self.replot()

        scale = self.axis(QwtPlot.yLeft)
        scale.setBaselineDist(10)
        QWhatsThis.add(
            scale, 'Selecting a value at the scale will insert a new curve.')

        self.__colorBar = ColorBar(Qt.Vertical, scale)
        self.__colorBar.setRange(Qt.red, Qt.darkBlue)
        self.__colorBar.setFocusPolicy(QWidget.TabFocus)
        QWhatsThis.add(
            self.__colorBar,
            'Selecting a color will change the background of the plot.')
        self.connect(
            self.__colorBar, PYSIGNAL("colorSelected"), self.setCanvasColor)
        scale.installEventFilter(self)

        scale = self.axis(QwtPlot.xBottom)
        scale.setBaselineDist(12)
        QWhatsThis.add(
            scale, 'Selecting a value at the scale will insert a new curve.')
        
        self.__slider = QSlider(0, 100, 10, 50, Qt.Horizontal, scale)
        self.__slider.setTracking(True)
        QWhatsThis.add(
            self.__slider,
            'With this slider you can move the visible area.')
        self.connect(
            self.__slider, SIGNAL('valueChanged(int)'), self.sliderMoved)

        scale.installEventFilter(self)

    def setCanvasColor(self, color):
        self.setCanvasBackground(color)
        self.replot()

    def sliderMoved(self):
        pos = self.__slider.sliderRect().center().x()
        range = self.__slider.width()
        base = 50.0 - 100.0 * pos / range
        self.setAxisScale(QwtPlot.xBottom, base, base + 100)
        self.replot()

    def eventFilter(self, object, event):
        if event.type() == QEvent.Resize:
            assert object.inherits("QwtScale")
            size = event.size()
            if object.position() == QwtScale.Left:
                margin = 2
                x = size.width() - object.baseLineDist() + margin
                w = object.baseLineDist() - 2 * margin
                y = object.startBorderDist()
                h = (size.height()
                     - object.startBorderDist() - object.endBorderDist())
                self.__colorBar.setGeometry(x, y, w, h)
            elif object.position() == QwtScale.Bottom:
                x = object.startBorderDist()
                w = (size.width() -
                     object.startBorderDist() - object.endBorderDist())
                y = 0
                h = object.baseLineDist()
                self.__slider.setGeometry(x, y, w, h)
        return QwtPlot.eventFilter(self, object, event)
    

    def insertCurve(self, axis, base):
        if axis == QwtPlot.yLeft or axis == QwtPlot.yRight:
            o = Qt.Horizontal
        else:
            o = Qt.Vertical
            
        self.__insertCurve(o, QColor(Qt.red), base)
        self.replot()
        

    def __insertCurve(self, orientation, color, base):
        curve = QwtPlotCurve(self)

        curve.setPen(QPen(color))
        curve.setSymbol(QwtSymbol(QwtSymbol.Ellipse, QBrush(Qt.gray),
                                  QPen(color), QSize(8, 8)))

        fixed = base*ones(10, Float)
        changing = arange(0, 95.0, 10.0, Float) + 5.0
        if orientation == Qt.Horizontal:
            curve.setData(changing, fixed)
        else:
            curve.setData(fixed, changing)
        QwtPlot.insertCurve(self, curve)


class CanvasPicker(QObject):
    
    def __init__(self, plot):
        QObject.__init__(self, plot)
        self.__selectedCurve = -1
        self.__selectedPoint = -1
        self.__plot = plot
        # prevent recursive painting
        self.__inPaint = False

        canvas = plot.canvas()
        canvas.installEventFilter(self)
        canvas.setFocusPolicy(QWidget.StrongFocus)
        canvas.setFocusIndicator(QwtPlotCanvas.ItemFocusIndicator)
        canvas.setFocus()
        canvas.setCursor(Qt.pointingHandCursor)
        
        QWhatsThis.add(
            canvas,
            'All points can be moved using the left mouse button '
            'or with these keys:\n\n'
            '- Up:\t\tSelect next curve\n'
            '- Down:\t\tSelect previous curve\n'
            '- Left, ´-´:\tSelect next point\n'
            '- Right, ´+´:\tSelect previous point\n'
            '- 7, 8, 9, 4, 6, 1, 2, 3:\tMove selected point'
            )

        self.__shiftCurveCursor(True)

    # __init__()

    def eventFilter(self, object, event):
        if event.type() == QEvent.FocusIn:
            self.__showCursor(True)
        elif event.type() == QEvent.FocusOut:
            self.__showCursor(False)
        elif event.type() == QEvent.Paint:
            assert object.inherits("QwtPlotCanvas")
            if not self.__inPaint and object.hasFocus():
                self.__inPaint = True
                object.repaint(event.rect().x(),
                               event.rect().y(),
                               event.rect().width(),
                               event.rect().height(),
                               False)
                self.__inPaint = False
                self.__showCursor(True)
                return True
            return QwtPlot.eventFilter(self, object, event)

        elif event.type() == QEvent.MouseButtonPress:
            self.__select(event.pos())
            return True

        if event.type() == QEvent.MouseMove:
            self.__move(event.pos())
            return True

        if event.type() == QEvent.KeyPress:
            delta = 5
            key = event.key()
            if key == Qt.Key_Up:
                self.__shiftCurveCursor(True)
                return True
            if key == Qt.Key_Down:
                self.__shiftCurveCursor(False)
                return True
            if key == Qt.Key_Right or key == Qt.Key_Plus:
                if self.__selectedCurve < 0:
                    self.__shiftCurveCursor(True)
                else:
                    self.__shiftPointCursor(True)
                return True
            if key == Qt.Key_Right or key == Qt.Key_Plus:
                if self.__selectedCurve < 0:
                    self.__shiftCurveCursor(True)
                else:
                    self.__shiftPointCursor(False)
                return True
            if key == Qt.Key_Left or key == Qt.Key_Minus:
                if self.__selectedCurve < 0:
                    self.__shiftCurveCursor(True)
                else:
                    self.__shiftPointCursor(False)
                return True

            if key == Qt.Key_1:
                self.__moveBy(-delta, delta)
            elif key == Qt.Key_2:
                self.__moveBy(0, delta)
            elif key == Qt.Key_3:
                self.__moveBy(delta, delta)
            elif key == Qt.Key_4:
                self.__moveBy(-delta, 0)
            elif key == Qt.Key_6:
                self.__moveBy(delta, 0)
            elif key == Qt.Key_7:
                self.__moveBy(-delta, -delta)
            elif key == Qt.Key_8:
                self.__moveBy(0, -delta)
            elif key == Qt.Key_9:
                self.__moveBy(delta, -delta)
        
        return QwtPlot.eventFilter(self, object, event)

    # eventFilter()

    def __select(self, pos):
        curve, dist, x, y, point = self.__plot.closestCurve(pos.x(), pos.y()) 

        if curve >= 0 and dist < 10:
            self.__selectedCurve = curve
            self.__selectedPoint = point
            self.__showCursor(True)
        else:
            self.__showCursor(False)
            self.__selectedCurve = -1
            self.__selectedPoint = -1

    def __move(self, pos):
        curve = self.__plot.curve(self.__selectedCurve)
        if not curve:
            return

        xData = zeros(curve.dataSize(), Float)
        yData = zeros(curve.dataSize(), Float)

        for i in range(curve.dataSize()):
            if i == self.__selectedPoint:
                xData[i] = self.__plot.invTransform(curve.xAxis(), pos.x())
                yData[i] = self.__plot.invTransform(curve.yAxis(), pos.y())
            else:
                xData[i] = curve.x(i)
                yData[i] = curve.y(i)
            
        curve.setData(xData, yData)
        self.__plot.replot()
        self.__showCursor(True)

    # __move()

    def __moveBy(self, dx, dy):
        if dx == 0 and dy == 0:
            return

        curve = self.__plot.curve(self.__selectedCurve)
        if not curve:
            return

        x = self.__plot.transform(
            curve.xAxis(), curve.x(self.__selectedPoint)) + dx
        y = self.__plot.transform(
            curve.yAxis(), curve.y(self.__selectedPoint)) + dy
        self.__move(QPoint(x, y))

    # __moveBy()

    def __showCursor(self, enable):
        curve = self.__plot.curve(self.__selectedCurve)
        if not curve:
            return

        painter= QPainter(self.__plot.canvas())
        painter.setClipping(True)
        painter.setClipRect(self.__plot.canvas().contentsRect())
        if enable:
            painter.setRasterOp(Qt.NotROP)

        curve.draw(
            painter,
            self.__plot.canvasMap(curve.xAxis()),
            self.__plot.canvasMap(curve.yAxis()),
            self.__selectedPoint, self.__selectedPoint)

    # __showCursor()
    
    def __shiftPointCursor(self, up):
        curve = self.__plot.curve(self.__selectedCurve)
        if not curve:
            return

        if up:
            index = self.__selectedPoint + 1
        else:
            index = self.__selectedPoint - 1

        index = (index + curve.dataSize()) % curve.dataSize()
        if index != self.__selectedPoint:
            self.__showCursor(False)
            self.__selectedPoint = index
            self.__showCursor(True)

    # __shiftPointCursor()
   
    def __shiftCurveCursor(self, up):
        keys = self.__plot.curveKeys()

        index = 0
        if self.__selectedCurve >= 0:
            for index in range(len(keys)):
                if self.__selectedCurve == keys[index]:
                    if up:
                        index += 1
                    else:
                        index -= 1
                    break

        key = keys[index % len(keys)]
        if self.__selectedCurve != key:
            self.__showCursor(False)
            self.__selectedPoint = 0
            self.__selectedCurve = key
            self.__showCursor(True)

    # __shiftCurveCursor()

# class CanvasPicker


class ScalePicker(QObject):
    def __init__(self, plot):
        QObject.__init__(self, plot)
        for i in range(QwtPlot.axisCnt):
            scale = plot.axis(i)
            if scale:
                scale.installEventFilter(self)

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress):
            self.__mouseClicked(object, event.pos())
            return True
        return QObject.eventFilter(self, object, event)
                                

    def __mouseClicked(self, scale, pos):
        rect = self.__scaleRect(scale)

        margin = 10
        rect.setRect(rect.x() - margin, rect.y() - margin,
                     rect.width() + 2 * margin, rect.height() +  2 * margin)

        if rect.contains(pos):
            value = 0.0
            axis = -1

        sd = scale.scaleDraw()
        if scale.position() == QwtScale.Left:
            value = sd.invTransform(pos.y())
            axis = QwtPlot.yLeft
        elif scale.position() == QwtScale.Right:
            value = sd.invTransform(pos.y())
            axis = QwtPlot.yRight
        elif scale.position() == QwtScale.Bottom:
            value = sd.invTransform(pos.x())
            axis = QwtPlot.xBottom
        elif scale.position() == QwtScale.Top:
            value = sd.invTransform(pos.x())
            axis = QwtPlot.xBottom

        self.emit(PYSIGNAL("clicked"), (axis, value))

    # __mouseClicked()
 
    def __scaleRect(self, scale):
        bld = scale.baseLineDist()
        mjt = scale.scaleDraw().majTickLength()
        sbd = scale.startBorderDist()
        ebd = scale.endBorderDist()

        if scale.position() == QwtScale.Left:
            return QRect(scale.width() - bld - mjt, sbd,
                         mjt, scale.height() - sbd - ebd)
        elif scale.position() == QwtScale.Right: 
            return QRect(bld, sbd,mjt, scale.height() - sbd - ebd)
        elif scale.position() == QwtScale.Bottom:
            return QRect(sbd, bld, scale.width() - sbd - ebd, mjt)
        elif scale.position() == QwtScale.Top:
            return QRect(sbd, scale.height() - bld - mjt,
                         scale.width() - sbd - ebd, mjt)
        else:
            return QRect()

    # __scaleRect

# class ScalePicker


def make():
    demo = QMainWindow()

    toolBar = QToolBar(demo)
    QWhatsThis.whatsThisButton(toolBar)

    plot = Plot(demo)
    demo.setCentralWidget(plot)
    QWhatsThis.add(
        plot,
        'An useless plot to demonstrate how to use event filtering.\n\n'
        'You can click on the color bar, the scales or move the slider.\n'
        'All points can be moved using the mouse or the keyboard.')


    CanvasPicker(plot)
    scalePicker = ScalePicker(plot)
    QObject.connect(scalePicker, PYSIGNAL("clicked"), plot.insertCurve)

    demo.resize(540, 400)
    demo.show()
    return demo

# make()

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

# Admire!
if __name__ == '__main__':
    main(sys.argv)
