"""qwt.qplt

Provides a Command Line Interpreter friendly interface to QwtPlot.
"""
#
# Copyright (C) 2003 Gerard Vermeulen
#
# This file is part of PyQwt
#
# PyQwt is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# PyQwt is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU  General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, Gerard Vermeulen gives permission to
# link PyQwt dynamically with commercial, non-commercial or educational
# versions of Qt, PyQt and sip, and distribute PyQwt in this form, provided
# that equally powerful versions of Qt, PyQt and sip have been released under
# the terms of the GNU General Public License.
#
# If PyQwt is dynamically linked with commercial, non-commercial or educational
# versions of Qt, PyQt and sip, PyQwt becomes a free plug-in for a non-free
# program.


import sys

from Numeric import *
from qt import *
from qwt import *
from types import *

from grace import GracePlotter

"""
__all__ = [
    # classes
    'Plot',
    'Curve',
    'Symbol',
    'Axis',
    'Brush',
    'Pen',
    # colors
    'Black',
    'Blue',
    'Cyan',
    'DarkBlue',
    'DarkCyan',
    'DarkGray',
    'DarkGreen',
    'DarkMagenta',
    'DarkRed',
    'DarkYellow',
    'Gray',
    'Green',
    'LightGray',
    'Magenta',
    'Red',
    'White',
    'Yellow',
    # axis orientation
    'Left',
    'Right',
    'Bottom',
    'Top',
    # axis option
    'PlainAxis',
    'IncludeRef',
    'Symmetric',
    'Floating',
    'Inverted',
    'Logarithmic',
    # symbol style
    'NoSymbol',
    'Circle',
    'Square',
    'Diamond',
    # line style
    'NoLine',
    'SolidLine',
    'DashLine',
    'DotLine',
    'DashDotLine',
    'DashDotDotLine',
    ]
"""
# colors
Black       = Qt.black
Blue        = Qt.blue
Cyan        = Qt.cyan
DarkBlue    = Qt.darkBlue
DarkCyan    = Qt.darkCyan
DarkGray    = Qt.darkGray
DarkGreen   = Qt.darkGreen
DarkMagenta = Qt.darkMagenta
DarkRed     = Qt.darkRed
DarkYellow  = Qt.darkYellow
Gray        = Qt.gray
Green       = Qt.green
LightGray   = Qt.lightGray
Magenta     = Qt.magenta
Red         = Qt.red
White       = Qt.white
Yellow      = Qt.yellow



## class PositonMarker(QwtPlotMarker):
##     def __init__(self, *args):
##         QwtPlotMarker.__init__(self, *args)

##     def draw(self, painter, x, y, rect):
##         pass
        
    
class Plot(QwtPlot):
    """Sugar coating for QwtPlot.
    """
    def __init__(self, *args):
        """Constructor.

        Usage: plot = Plot(*args)
        
        Plot takes any number of optional arguments. The interpretation
        of each optional argument depend on its data type:
        (1) Axis -- enables the axis.
        (2) Curve -- plots a curve.
        (3) string or QString -- sets the title.
        (4) tuples of 2 integer -- sets the size.
        """

        self.size = (600, 400)
        # get an optional parent widget
        parent = None
        for arg in args:
            if isinstance(arg, QWidget):
                parent = arg
                self.size = None
        QwtPlot.__init__(self, parent)
        font = QFont('verdana')
        if font.exactMatch():
            self.setFont(font)

        # user interface
        self.setCanvasBackground(Qt.white)
        self.setOutlinePen(QPen(Qt.black))
        self.setAutoLegend(1)
        self.setLegendPos(Qwt.Right)

        # zoom
        self.zoomStack = []
        self.zoomState = None
        
        # initialization
        for arg in args:
            if isinstance(arg, Axis):
                self.plotAxis(arg.orientation, arg.options, arg.title)
            elif isinstance(arg, Curve):
                self.plotCurve(arg)
            elif (isinstance(arg, StringType) or isinstance(arg, QString)):
                self.setTitle(arg)
                self.setTitleFont(
                    QFont(QFontInfo(self.font()).family(), 14, QFont.Bold))
            elif (isinstance(arg, tuple) and len(tuple) == 2
                  and isinstance(arg[0], int) and isinstance(arg[1], int)):
                self.size = arg
            elif (isinstance(arg, QWidget)):
                pass
                #print "Plot() fails to accept %s." % arg
            else:
                print "Plot() fails to accept %s." % arg

        if self.size:
            apply(self.resize, self.size)
        self.replot()

        self.connect(self, SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)
        self.connect(self, SIGNAL('plotMousePressed(const QMouseEvent&)'),
                     self.onMousePressed)
        self.connect(self, SIGNAL('plotMouseReleased(const QMouseEvent&)'),
                     self.onMouseReleased)
        self.connect(self, SIGNAL("legendClicked(long)"), self.toggleCurve)
        self.show()

    # __init__()

    def __getattr__(self, attr):
        if hasattr(QwtPlot, attr):
            return getattr(self.sipThis, attr)
        else:
            raise AttributeError, ('%s has no attribute named %s'
                                   % (self.__class__.__name__, attr)
                                   )
    # __getattr__()
        
    def plot(self, *args):
        for arg in args:
            if isinstance(arg, Curve):
                self.plotCurve(arg)
            else:
                print "Plot.plot() fails to accept %s." % arg
        self.replot()

    # plot()

    def plotAxis(self, orientation, options, title):
        self.enableAxis(orientation)
        self.setAxisOptions(orientation, options)
        if title:
            self.setAxisTitle(orientation, title)
            self.setAxisTitleFont(
                orientation,
                QFont(QFontInfo(self.font()).family(), 12, QFont.Bold))

    # plotAxis()

    def plotCurve(self, curve):
        key = self.insertCurve(curve.name, curve.xAxis, curve.yAxis)
        if curve.pen:
            self.setCurvePen(key, curve.pen)
        else:
            self.setCurveStyle(key, QwtCurve.NoCurve)
        if curve.symbol:
            self.setCurveSymbol(key, curve.symbol)
        self.setCurveData(key, curve.x, curve.y)

    # plotCurve()

    def formatCoordinates(self, x, y):
        result = []
        todo = ((QwtPlot.xBottom, "x0=%+.6g", x),
                (QwtPlot.yLeft,   "y0=%+.6g", y),
                (QwtPlot.xTop,    "x1=%+.6g", x),
                (QwtPlot.yRight,  "y1=%+.6g", y))
        for axis, template, value in todo:
            if self.axisEnabled(axis):
                value = self.invTransform(axis, value)
                result.append(template % value)
        return result

    # formatCoordinates()

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
            for axis in [QwtPlot.xBottom]:
                if self.axisEnabled(axis):
                    xmin = self.invTransform(axis, xmin)
                    xmax = self.invTransform(axis, xmax)
            for axis in [QwtPlot.yLeft]:
                if self.axisEnabled(axis):
                    ymin = self.invTransform(axis, ymin)
                    ymax = self.invTransform(axis, ymax)
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
            
        for axis in [QwtPlot.xBottom]:
            if self.axisEnabled(axis):
                self.setAxisScale(axis, xmin, xmax)
        for axis in [QwtPlot.yLeft]:
            if self.axisEnabled(axis):
                self.setAxisScale(axis, ymin, ymax)
        self.replot()

    # onMouseReleased()

    def toggleCurve(self, key):
        curve = self.curve(key)
        if curve:
            curve.setEnabled(not curve.enabled())
            self.replot()

    # toggleCurve()

    def gracePlot(self):
        g = GracePlotter(debug = 0)
        g('subtitle "%s"' % self.title())
        g('g0 on; with g0')
        if self.axisEnabled(QwtPlot.xBottom):
            axisScale = self.axisScale(QwtPlot.xBottom)
            min = axisScale.lBound()
            max = axisScale.hBound()
            majStep = minStep = axisScale.majStep()
            majStep *= 2
            g('world xmin %g; world xmax %g' % (min, max))
            g('xaxis tick major %12.6f; xaxis tick minor %12.6f' %
              (majStep, minStep))
            g('xaxis label "%s"; xaxis label char size 1.5' %
              self.axisTitle(QwtPlot.xBottom))
        if self.axisEnabled(QwtPlot.yLeft):
            axisScale = self.axisScale(QwtPlot.yLeft)
            min = axisScale.lBound()
            max = axisScale.hBound()
            majStep = minStep = axisScale.majStep()
            majStep *= 2
            g('world ymin %g; world ymax %g' % (min, max))
            g('yaxis tick major %12.6f; yaxis tick minor %12.6f' %
              (majStep, minStep))
            g('yaxis label "%s"; yaxis label char size 1.5' %
              self.axisTitle(QwtPlot.yLeft))
        g.flush()
        keys = self.curveKeys()
        for key in keys:
            index = keys.index(key)
            curve = self.curve(key)
            if not curve.enabled():
                continue
            g('s%s on' % index)
            g('s%s legend "%s"' % (index, curve.title()))
            if curve.symbol().style():
                g('s%s symbol 1;s%s symbol size 0.4;s%s symbol fill pattern 1'
                  % (index, index, index))
            if curve.style():
                g('s%s line linestyle 1' % index)
            else:
                g('s%s line linestyle 0' % index)
            for i in range(curve.dataSize()):
                g('g0.s%s point %g, %g'  % (index, curve.x(i), curve.y(i)))
                g.flush()
        g('redraw')
        g.flush()
        #g.wait()
        
    # gracePlot()
        
# class Plot


class Curve:
    """Sugar coating for QwtPlotCurve.
    """
    def __init__(self, x, y, *args):
        """Constructor.

        Usage: curve = Curve(x, y, *args)
        
        Curve takes two obligatory arguments followed by any number of
        optional arguments. The arguments 'x' and 'y' must be sequences
        of floats. The interpretation of each optional argument depends
        on its data type:
        (1) Axis -- attaches an axis to the curve.
        (2) Pen -- sets the pen to connect the data points.
        (3) Symbol -- sets the symbol to draw the data points.
        (4) string or QString -- sets the title of the curve.
        """
        self.x = x # must be sequence of floats, typecode()?
        self.y = y # must be sequence of floats
        self.name = ""
        self.xAxis = QwtPlot.xBottom
        self.yAxis = QwtPlot.yLeft
        self.symbol = None
        self.pen = None

        for arg in args:
            if isinstance(arg, AxisOrientation):
                if arg.orientation in (QwtPlot.xBottom, QwtPlot.xTop):
                    self.xAxis = arg.orientation
                elif arg.orientation in (QwtPlot.yLeft, QwtPlot.yRight):
                    self.yAxis = arg.orientation
                else:
                    raise FIXME
            elif isinstance(arg, Pen):
                self.pen = arg
            elif (isinstance(arg, StringType) or isinstance(arg, QString)):
                self.name = arg
            elif isinstance(arg, Symbol):
                self.symbol = arg
            else:
                print "Curve fails to accept %s." % arg

        if not self.symbol and not self.pen:
            self.pen = QPen()

    # __init__()


class AxisOption:
    def __init__(self, option):
        self.option = option
    # FIXME 

# class AxisOption


PlainAxis    = QwtAutoScale.None
IncludeRef   = QwtAutoScale.IncludeRef
Symmetric    = QwtAutoScale.Symmetric
Floating     = QwtAutoScale.Floating
Logarithmic  = QwtAutoScale.Logarithmic
Inverted     = QwtAutoScale.Inverted

class AxisOrientation:
    def __init__(self, orientation):
        self.orientation = orientation

# class AxisOrientation


Left   = AxisOrientation(QwtPlot.yLeft)
Right  = AxisOrientation(QwtPlot.yRight)
Bottom = AxisOrientation(QwtPlot.xBottom)
Top    = AxisOrientation(QwtPlot.xTop)

class Axis:
    def __init__(self, *args):
        """Constructor.

        Usage: axis = Axis(*args)
        
        Axis takes any number of optional arguments. The interpretation
        of each optional argument depends on its data type:
        (1) AxisOrientation -- sets the orientation of the axis.
        (2) int -- sets the options of the axis.
        (3) string or QString -- sets the title of the axis.
        """
        self.options = PlainAxis
        self.title = ""
        for arg in args:
            if isinstance(arg, AxisOrientation):
                self.orientation = arg.orientation
            elif isinstance(arg, int):
                self.options = arg
            elif (isinstance(arg, StringType) or isinstance(arg, QString)):
                self.title = arg
            else:
                print "Axis() fails to accept %s." % arg

    # __init__()

# class Axis


class Brush:
    pass

# class Brush


class SymbolStyle:
    def __init__(self, style):
        self.style = style

    # __init__()

# class SymbolStyle

NoSymbol = SymbolStyle(QwtSymbol.None)
Circle   = SymbolStyle(QwtSymbol.Ellipse)
Square   = SymbolStyle(QwtSymbol.Rect)
Diamond  = SymbolStyle(QwtSymbol.Diamond)

class PenStyle:
    def __init__(self, style):
        self.style = style

    # __init__()

# class PenStyle


NoLine         = PenStyle(Qt.NoPen) 
SolidLine      = PenStyle(Qt.SolidLine)
DashLine       = PenStyle(Qt.DashLine)
DotLine        = PenStyle(Qt.DotLine)
DashDotLine    = PenStyle(Qt.DashDotLine)
DashDotDotLine = PenStyle(Qt.DashDotDotLine)


class Symbol(QwtSymbol):
    """Sugar coating for QwtSymbol.
    """
    def __init__(self, *args):
        """Constructor.

        Usage: symbol = Axis(*args)
        
        Symbol takes any number of optional arguments. The interpretation
        of each optional argument depends on its data type:
        (1) QColor -- sets the fill color of the symbol.
        (2) SymbolStyle -- sets the style of the symbol.
        (3) int -- sets the size of the symbol.
        """
        QwtSymbol.__init__(self)
        self.setSize(5)
        for arg in args:
            if isinstance(arg, QColor):
                brush = self.brush()
                brush.setColor(arg)
                self.setBrush(brush)
            elif isinstance(arg, SymbolStyle):
                self.setStyle(arg.style)
            elif isinstance(arg, int):
                self.setSize(arg)
            else:
                print "Symbol fails to accept %s." %  arg

    # __init__()

# class Symbol


class Pen(QPen):
    def __init__(self, *args):
        """Constructor.

        Usage: pen = Pen(*args)
        
        Pen takes any number of optional arguments. The interpretation
        of each optional argument depends on its data type:
        (1) PenStyle -- sets the style of the pen.
        (2) QColor -- sets the color of the pen.
        (3) int -- sets the width of the pen.
        """
        QPen.__init__(self)
        for arg in args:
            if isinstance(arg, PenStyle):
                self.setStyle(arg.style)
            elif isinstance(arg, QColor):
                self.setColor(arg)
            elif isinstance(arg, int):
                self.setWidth(arg)
            else:
                print "Pen fails to accept %s." % arg

    # __init__()

# class Pen


print_xpm = ['32 32 12 1',
             'a c #ffffff',
             'h c #ffff00',
             'c c #ffffff',
             'f c #dcdcdc',
             'b c #c0c0c0',
             'j c #a0a0a4',
             'e c #808080',
             'g c #808000',
             'd c #585858',
             'i c #00ff00',
             '# c #000000',
             '. c None',
             '................................',
             '................................',
             '...........###..................',
             '..........#abb###...............',
             '.........#aabbbbb###............',
             '.........#ddaaabbbbb###.........',
             '........#ddddddaaabbbbb###......',
             '.......#deffddddddaaabbbbb###...',
             '......#deaaabbbddddddaaabbbbb###',
             '.....#deaaaaaaabbbddddddaaabbbb#',
             '....#deaaabbbaaaa#ddedddfggaaad#',
             '...#deaaaaaaaaaa#ddeeeeafgggfdd#',
             '..#deaaabbbaaaa#ddeeeeabbbbgfdd#',
             '.#deeefaaaaaaa#ddeeeeabbhhbbadd#',
             '#aabbbeeefaaa#ddeeeeabbbbbbaddd#',
             '#bbaaabbbeee#ddeeeeabbiibbadddd#',
             '#bbbbbaaabbbeeeeeeabbbbbbaddddd#',
             '#bjbbbbbbaaabbbbeabbbbbbadddddd#',
             '#bjjjjbbbbbbaaaeabbbbbbaddddddd#',
             '#bjaaajjjbbbbbbaaabbbbadddddddd#',
             '#bbbbbaaajjjbbbbbbaaaaddddddddd#',
             '#bjbbbbbbaaajjjbbbbbbddddddddd#.',
             '#bjjjjbbbbbbaaajjjbbbdddddddd#..',
             '#bjaaajjjbbbbbbjaajjbddddddd#...',
             '#bbbbbaaajjjbbbjbbaabdddddd#....',
             '###bbbbbbaaajjjjbbbbbddddd#.....',
             '...###bbbbbbaaajbbbbbdddd#......',
             '......###bbbbbbjbbbbbddd#.......',
             '.........###bbbbbbbbbdd#........',
             '............###bbbbbbd#.........',
             '...............###bbb#..........',
             '..................###...........']


class IPlot(QMainWindow):
    """A QMainWindow widget with a Plot widget as central widget.

    It provides:
    (1) a toolbar for printing and piping into Grace.
    (2) legend control to (un)hide curves.
    (3) mouse tracking to display the coordinates in the status bar.
    (4) an infinite stack of zoom region. Dragging the mouse with the
        left button pressed selects a new zoom region. Right clicking
        pops the previous zoom level from the stack.
    """
    
    def __init__(self, *args):
        """Constructor.

        Usage: plot = Plot(*args)
        
        Plot takes any number of optional arguments. The interpretation
        of each optional argument depend on its data type:
        (1) Axis -- enables the axis.
        (2) Curve -- plots a curve.
        (3) string or QString -- sets the title.
        (4) tuples of 2 integer -- sets the size.
        """
        QMainWindow.__init__(self)
        self.__plot = Plot(self, *args)
        self.setCentralWidget(self.__plot)

        self.toolBar = QToolBar(self)

        printButton = QToolButton(self.toolBar)
        printButton.setTextLabel("Print")
        printButton.setPixmap(QPixmap(print_xpm))
        self.toolBar.addSeparator()

        graceButton = QToolButton(self.toolBar)
        graceButton.setTextLabel("Grace")
        graceButton.setUsesTextLabel(1)
        self.toolBar.addSeparator()

        #helpButton = QToolBar(self.toolBar)
        #helpButton.setTextLabel("Help")

        self.connect(printButton, SIGNAL('clicked()'), self.printPlot)
        self.connect(graceButton, SIGNAL('clicked()'), self.gracePlot)

        self.statusBar().message("Move the mouse within the plot canvas"
                                 " to show the cursor position")
        self.__plot.canvas().setMouseTracking(1)
        self.connect(self.__plot, SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)

        self.resize(700, 500)
        self.show()

    def printPlot(self):
        try:
            p = QPrinter(QPrinter.HighResolution)
        except AttributeError:
            p = QPrinter()
        p.setColorMode(QPrinter.Color)
        p.setOutputToFile(True)
        if p.setup():
            self.__plot.printPlot(p)

    def onMouseMoved(self, e):
        self.statusBar().message(
            ' -- '.join(self.formatCoordinates(e.pos().x(), e.pos().y())))
        
    def __getattr__(self, attr):
        if hasattr(QMainWindow, attr):
            return getattr(self.sipThis, attr)
        elif hasattr(self.__plot, attr):
            return getattr(self.__plot, attr)
        else:
            raise AttributeError, ('%s has no attribute named %s'
                                   % (self.__class__.__name__, attr)
                                   )
        
        
# Admire!
from Numeric import *
import random

def standard_map(x, y, kappa, n):
    xs = zeros(n, Float)
    ys = zeros(n, Float)
    for i in range(n):
        xs[i] = x
        ys[i] = y
        xn = y-kappa*sin(2.0*pi*x)
        yn = x+y
        if (xn > 1.0) or (xn < 0.0):
            x = xn-floor(xn)
        else:
            x = xn
        if (yn > 1.0) or (yn < 0.0):
            y = yn-floor(yn)
        else:
            y = yn
    return xs, ys
        
        
def testIPlot():
    x = random.random()
    y = random.random()
    kappa = random.random()
    print "x = %s, y = %s, kappa = %s" % (x, y, kappa)
    xs, ys = standard_map(x, y, kappa, 1 << 16)
    p = IPlot(Curve(xs, ys, Symbol(Circle, Red), "standard_map"),
              ("PyQwt demo based on Qwt-%s (http://qwt.sf.net)"
               % QWT_VERSION_STR))
    return p


def testPlot():
    x = arange(-2*pi, 2*pi, 0.01)
    p = Plot(Curve(x, cos(x), Pen(Magenta, 2), "cos(x)"),
             Axis(Bottom, "x axis"),
             Axis(Left, "y axis"),
             Axis(Right, Logarithmic),
             Curve(x, exp(x), Pen(Red), "exp(x)", Right),
             ("PyQwt demo based on Qwt-%s (http://qwt.sf.net)"
              % QWT_VERSION_STR))
    x = x[0:-1:10]
    p.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),
           Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))
    return p


if __name__ == '__main__':
    # HACK to allow execfile('qplt.py') from a PyQt application (PyCute.py)
    try: 
        qApp.argc() 
        p = testPlot()
    except RuntimeError:
        a = QApplication(sys.argv)
        p = testIPlot()
        a.setMainWidget(p)
        a.exec_loop()

    
