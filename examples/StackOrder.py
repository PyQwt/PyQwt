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
                            'use the ?-pointer for help',
                            self)
        self.plot.plotLayout().setCanvasMargin(0)
        self.plot.plotLayout().setAlignCanvasToScales(True)
        self.setCentralWidget(self.plot)

        self.__initTracking()
        self.__initZooming()
        self.__initToolBar()
        
        # Finalize
        self.counter.setValue(10)
        self.go(self.counter.value())

    # __init__()

    def __initTracking(self):
        """Initialize tracking
        """        
        self.connect(self.plot,
                     SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)
        self.plot.canvas().setMouseTracking(True)
        self.statusBar().message(
            'Plot cursor movements are tracked in the status bar')

    # __initTracking()

    def onMouseMoved(self, e):
        self.statusBar().message(
            'x = %+.6g, y = %.6g'
            % (self.plot.invTransform(QwtPlot.xBottom, e.pos().x()),
               self.plot.invTransform(QwtPlot.yLeft, e.pos().y())))

    # onMouseMoved()
    
    def __initZooming(self):
        """Initialize zooming
        """
        self.zoomer = QwtPlotZoomer(QwtPlot.xBottom,
                                    QwtPlot.yLeft,
                                    QwtPicker.DragSelection,
                                    QwtPicker.AlwaysOff,
                                    self.plot.canvas())
        self.zoomer.setRubberBandPen(QPen(Qt.black))

    # __initZooming()
       
    def setZoomerMousePattern(self, index):
        """Set the mouse zoomer pattern.
        """
        if index == 0:
            pattern = [
                QwtEventPattern.MousePattern(Qt.LeftButton, Qt.NoButton),
                QwtEventPattern.MousePattern(Qt.MidButton, Qt.NoButton),
                QwtEventPattern.MousePattern(Qt.RightButton, Qt.NoButton),
                QwtEventPattern.MousePattern(Qt.LeftButton, Qt.ShiftButton),
                QwtEventPattern.MousePattern(Qt.MidButton, Qt.ShiftButton),
                QwtEventPattern.MousePattern(Qt.RightButton, Qt.ShiftButton),
                ]
            self.zoomer.setMousePattern(pattern)
        elif index in (1, 2, 3):
            self.zoomer.initMousePattern(index)
        else:
            raise ValueError, 'index must be in (0, 1, 2, 3)'

    # setZoomerMousePattern()

    def __initToolBar(self):
        """Initialize the toolbar
        """
        
        self.toolBar = QToolBar(self)

        QLabel('Pen', self.toolBar)
        self.penComboBox = QComboBox(self.toolBar)
        for name in self.table.keys():
            self.penComboBox.insertItem(name)
        self.penComboBox.setCurrentItem(
            random.randint(0, self.penComboBox.count()-1))
        self.penComboBox.setMaximumWidth(75)
        self.toolBar.addSeparator()

        QLabel('Brush', self.toolBar)
        self.brushComboBox = QComboBox(self.toolBar)
        for name in self.table.keys():
            self.brushComboBox.insertItem(name)
        self.brushComboBox.setCurrentItem(
            random.randint(0, self.brushComboBox.count()-1))
        self.brushComboBox.setMaximumWidth(75)
        self.toolBar.addSeparator()

        QLabel('Bars', self.toolBar)
        self.counter = QwtCounter(self.toolBar)
        self.counter.setRange(0, 10000, 1)
        self.counter.setNumButtons(3)
        self.toolBar.addSeparator()

        QLabel('Mouse', self.toolBar)
        mouseComboBox = QComboBox(self.toolBar)
        for name in ('3 buttons (PyQwt)',
                     '1 button',
                     '2 buttons',
                     '3 buttons (Qwt)'):
            mouseComboBox.insertItem(name)
        mouseComboBox.setCurrentItem(0)
        self.toolBar.addSeparator()
        self.setZoomerMousePattern(0)

        QWhatsThis.whatsThisButton(self.toolBar)

        QWhatsThis.add(
            self.plot.canvas(),
            'A QwtPlotZoomer lets you zoom infinitely deep\n'
            'by saving the zoom states on a stack.\n\n'
            'You can:\n'
            '- select a zoom region\n'
            '- unzoom all\n'
            '- walk down the stack\n'
            '- walk up the stack.\n\n'
            'One of the combo boxes in the toolbar lets you attach\n'
            'different sets of mouse events to those actions.'
            )
        
        QWhatsThis.add(
            self.penComboBox,
            'Select the pen color of the bars.'
            )
        
        QWhatsThis.add(
            self.brushComboBox,
            'Select the brush color of the bars'
            )
        
        QWhatsThis.add(
            self.counter,
            'Select the number of bars'
            )
        
        QWhatsThis.add(
            mouseComboBox,
            'Configure the zoomer mouse buttons.\n\n'
            '3 buttons (PyQwt style):\n'
            '- left-click & drag to zoom\n'
            '- middle-click to unzoom all\n'
            '- right-click to walk down the stack\n'
            '- shift-right-click to walk up the stack.\n'
            '1 button:\n'
            '- click & drag to zoom\n'
            '- control-click to unzoom all\n'
            '- alt-click to walk down the stack\n'
            '- shift-alt-click to walk up the stack.\n'
            '2 buttons:\n'
            '- left-click & drag to zoom\n'
            '- right-click to unzoom all\n'
            '- alt-left-click to walk down the stack\n'
            '- alt-shift-left-click to walk up the stack.\n'
            '3 buttons (Qwt style):\n'
            '- left-click & drag to zoom\n'
            '- right-click to unzoom all\n'
            '- middle-click to walk down the stack\n'
            '- shift-middle-click to walk up the stack.\n\n'
            'If some of those key combinations interfere with\n'
            'your Window manager, press the:\n'
            '- escape-key to unzoom all\n'
            '- minus-key to walk down the stack\n'
            '- plus-key to walk up the stack.'
            )

        self.connect(self.counter, SIGNAL('valueChanged(double)'), self.go)
        self.connect(self.penComboBox, SIGNAL('activated(int)'), self.go)
        self.connect(self.brushComboBox, SIGNAL('activated(int)'), self.go)
        self.connect(mouseComboBox, SIGNAL('activated(int)'),
                     self.setZoomerMousePattern)

    # __initToolBar()

    def go(self, x):
        """Create and plot a sequence of bars taking into account the controls
        """

        n = int(self.counter.value())
        penColor = self.table[str(self.penComboBox.currentText())]
        brushColor = self.table[str(self.brushComboBox.currentText())]
            
        self.plot.removeCurves()

        for i in range(n):
            curve = QwtBarCurve(self.plot, penColor, brushColor)
            key = self.plot.insertCurve(curve)
            self.plot.setCurveStyle(key, QwtCurve.UserCurve)
            self.plot.setCurveData(key, [i, i+1.4], [0.3*i, 5.0+0.3*i])

        if type(x) == type(0.0):
            # SIGNAL("valueChanged(double)")
            self.clearZoomStack()
        else:
            self.plot.replot()

    # go()

    def clearZoomStack(self):
        """Auto scale and clear the zoom stack
        """
        self.plot.setAxisAutoScale(QwtPlot.xBottom)
        self.plot.setAxisAutoScale(QwtPlot.yLeft)
        self.plot.replot()
        self.zoomer.setZoomBase()

    # clearZoomStack()
    
# class StackOrderDemo


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

def make():
    demo = QwtBarPlotDemo()
    demo.resize(600, 600)
    demo.show()
    return demo

# make()

# Admire!
if __name__ == '__main__':
    main(sys.argv)

