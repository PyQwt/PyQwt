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
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
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
import time

from Numeric import *
from qt import *
from qwt import *
from types import *

from grace import GracePlotter


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


class Plot(QwtPlot):
    """Sugar coating for QwtPlot.
    """
    def __init__(self, *args):
        """Constructor.

        Usage: plot = Plot([pattern,] *args)
        
        Plot takes any number of optional arguments. The interpretation
        of each optional argument depend on its data type:
        (1) Axis -- enables the axis.
        (2) Curve -- plots a curve.
        (3) QString or string -- sets the title.
        (4) integer -- attaches a set of mouse events to the zoomer actions
        (5) tuples of 2 integer -- sets the size.
        """

        self.size = (600, 400)

        # get an optional parent widget
        parent = None
        for arg in args:
            if isinstance(arg, QWidget):
                parent = arg
                self.size = None
        QwtPlot.__init__(self, parent)

        # font
        font = QFont('Verdana')
        if font.exactMatch():
            self.setFont(font)

        # user interface
        self.setCanvasBackground(Qt.white)
        self.setOutlinePen(QPen(Qt.black))
        self.setAutoLegend(1)
        self.setLegendPos(Qwt.Right)

        # zooming
        self.zoomers = []
        zoomer = QwtPlotZoomer(QwtPlot.xBottom,
                               QwtPlot.yLeft,
                               QwtPicker.DragSelection,
                               QwtPicker.AlwaysOff,
                               self.canvas())
        zoomer.setRubberBandPen(QPen(Black))
        self.zoomers.append(zoomer)
        zoomer = QwtPlotZoomer(QwtPlot.xTop,
                               QwtPlot.yRight,
                               QwtPicker.DragSelection,
                               QwtPicker.AlwaysOff,
                               self.canvas())
        zoomer.setRubberBand(QwtPicker.NoRubberBand)
        self.zoomers.append(zoomer)
        self.setZoomerMouseEventSet(0)

        # initialization
        for arg in args:
            if isinstance(arg, Axis):
                self.plotAxis(arg.orientation, arg.options, arg.title)
            elif isinstance(arg, Curve):
                self.plotCurve(arg)
            elif (isinstance(arg, QString) or isinstance(arg, StringType)):
                self.setTitle(arg)
                self.setTitleFont(
                    QFont(QFontInfo(self.font()).family(), 14, QFont.Bold))
            elif isinstance(arg, int):
                self.setZoomerMouseEventSet(arg)
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

        # connections
        self.connect(self, SIGNAL("legendClicked(long)"), self.toggleCurve)

        # finalize
        self.show()

    # __init__()

    def __getattr__(self, attr):
        """Inherit everything from QwtPlot.
        """
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

    # plot()

    def plotAxis(self, orientation, options, title):
        self.enableAxis(orientation)
        self.setAxisOptions(orientation, options)
        if title:
            self.setAxisTitle(orientation, title)
            self.setAxisTitleFont(
                orientation,
                QFont(QFontInfo(self.font()).family(), 12, QFont.Bold))
        self.clearZoomStack()

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
        self.clearZoomStack()

    # plotCurve()
    
    def clearZoomStack(self):
        """Force autoscaling and clear the zoom stack
        """
        self.setAxisAutoScale(QwtPlot.yLeft)
        self.setAxisAutoScale(QwtPlot.yRight)
        self.setAxisAutoScale(QwtPlot.xBottom)
        self.setAxisAutoScale(QwtPlot.xTop)
        self.replot()
        for zoomer in self.zoomers:
            zoomer.setZoomBase()

    # clearZoomStack()

    def setZoomerMouseEventSet(self, index):
        """Attach the QwtPlotZoomer actions to a set of mouse events.
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
            for zoomer in self.zoomers:
                zoomer.setMousePattern(pattern)
        elif index in (1, 2, 3):
            for zoomer in self.zoomers:
                zoomer.initMousePattern(index)
        else:
            raise ValueError, 'index must be in (0, 1, 2, 3)'
        self.__mouseEventSet = index

    # setZoomerMouseEventSet()

    def getZoomerMouseEventSet(self):
        return self.__mouseEventSet

    # getZoomerMouseEventSet()

    def formatCoordinates(self, x, y):
        """Format mouse coordinates as real world plot coordinates.
        """
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

    def toggleCurve(self, key):
        """Toggle a curve between hidden and shown.
        """
        curve = self.curve(key)
        if curve:
            curve.setEnabled(not curve.enabled())
            self.replot()

    # toggleCurve()

    def gracePlot(self, pause=0.2):
        """Clone the plot into Grace for very high quality hard copy output.

        Know bug: Grace does not scale the data correctly when Grace cannot
        cannot keep up with gracePlot.  This happens when it takes too long
        to load Grace in memory (exit the Grace process and try again) or
        when 'pause' is too short.
        """
        g = GracePlotter(debug = 0)
        g('subtitle "%s"' % self.title())
        for xAxis, yAxis, graph, xPlace, yPlace in [
            (QwtPlot.xBottom, QwtPlot.yLeft, 'g0', 'normal', 'normal'),
            (QwtPlot.xBottom, QwtPlot.yRight, 'g1', 'normal', 'opposite'),
            (QwtPlot.xTop, QwtPlot.yLeft, 'g2', 'opposite', 'normal'),
            (QwtPlot.xTop, QwtPlot.yRight, 'g3', 'opposite', 'opposite')
            ]:
            if not (self.axisEnabled(xAxis) and self.axisEnabled(yAxis)):
                continue
            g('%s on; with %s' % (graph, graph))

            # x-axes
            axisScale = self.axisScale(xAxis)
            min = axisScale.lBound()
            max = axisScale.hBound()
            majStep = minStep = axisScale.majStep()
            majStep *= 2
            g('world xmin %g; world xmax %g' % (min, max))
            g('xaxis label "%s"; xaxis label char size 1.5' %
              self.axisTitle(xAxis))
            g('xaxis label place %s' % xPlace)
            g('xaxis tick place %s' % xPlace)
            g('xaxis ticklabel place %s' % xPlace)
            time.sleep(pause)
            if self.axisOptions(xAxis) & QwtAutoScale.Logarithmic:
                #print 'log x-axis from %s to %s.' % (min, max)
                g('xaxes scale Logarithmic')
                g('xaxis tick major 10')
                g('xaxis tick minor ticks 9')
            else:
                #print 'lin x-axis from %s to %s.' % (min, max)
                g('xaxes scale Normal')
                g('xaxis tick major %12.6f; xaxis tick minor %12.6f'
                  % (majStep, minStep))

            # y-axes
            axisScale = self.axisScale(yAxis)
            min = axisScale.lBound()
            max = axisScale.hBound()
            majStep = minStep = axisScale.majStep()
            majStep *= 2
            g('world ymin %g; world ymax %g' % (min, max))
            g('yaxis label "%s"; yaxis label char size 1.5' %
              self.axisTitle(yAxis))
            g('yaxis label place %s' % yPlace)
            g('yaxis tick place %s' % yPlace)
            g('yaxis ticklabel place %s' % yPlace)
            time.sleep(pause)
            if self.axisOptions(yAxis) & QwtAutoScale.Logarithmic:
                #print 'log y-axis from %s to %s.' % (min, max)
                g('yaxes scale Logarithmic')
                g('yaxis tick major 10')
                g('yaxis tick minor ticks 9')
            else:
                #print 'lin y-axis from %s to %s.' % (min, max)
                g('yaxes scale Normal')
                g('yaxis tick major %12.6f; yaxis tick minor %12.6f' %
                  (majStep, minStep))

            # curves
            keys = self.curveKeys()
            for key in keys:
                index = keys.index(key)
                curve = self.curve(key)
                if not curve.enabled():
                    continue
                if not (xAxis == curve.xAxis() and yAxis == curve.yAxis()):
                    continue
                g('s%s legend "%s"' % (index, curve.title()))
                if curve.symbol().style():
                    g('s%s symbol 1;'
                      's%s symbol size 0.4;'
                      's%s symbol fill pattern 1'
                      % (index, index, index))
                if curve.style():
                    g('s%s line linestyle 1' % index)
                else:
                    g('s%s line linestyle 0' % index)
                for i in range(curve.dataSize()):
                    g('%s.s%s point %g, %g'
                      % (graph, index, curve.x(i), curve.y(i)))

        # finalize
        g('redraw')
        
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


print_xpm = [
    '32 32 12 1',
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
    '..................###...........',
    ]

grace_xpm = [
    '48 39 6 1',
    '  c #000000000000',
    '. c #FFFFFFFFFFFF',
    'X c #BEFBBEFBBEFB',
    'o c #51445144FFFF',
    'O c #FFFF14514103',
    '+ c #0000AAAA1861',
    '                                                ',
    ' .............................................. ',
    ' .............................................. ',
    ' ...............                  ............. ',
    ' .............................................. ',
    ' .................              ............... ',
    ' .............................................. ',
    ' .......                                 ...... ',
    ' ....... XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ...... ',
    ' ....... XXXXXXXXXXXXXXXXXXXXXXXXXXoXXXX ...... ',
    ' ..... . XXoooXX      XXXXXXXXXXXoooXXXX ...... ',
    ' .. .... XXXXXXXXXXXXXXXXXXXXXXXXoXooOXX ...... ',
    ' .. .... XXOOOXX     XXXXXXXXXXXXoXOoXXX ...... ',
    ' .. .... XXXXXXXXXXXXXXXXXXXXXXXoOOXooXX ...... ',
    ' .. .... XX+++XX     XXXXooXXXXOoXXXXoXX ...... ',
    ' .. .. . XXXXXXXXXXXXXXXoXoXXXOoXXXXXXXX ...... ',
    ' .. .... XXXXXXXXXXXXXXXoXoXOOooXXXXXXXX ...... ',
    ' .. .... XXXXXXXXXXXXXXoXXooXXoXXXXXXXXX ...... ',
    ' .. .... XXXXXXXoXXXXXooXOOoXoXXXXXXXXXX ...... ',
    ' .. .... XXXXXXooXXXXXoOOXXooXXXXXXXXXXX ...... ',
    ' .. .. . XXXXXXoXoXXXoOXXXXXXXXXXXXXXXXX ...... ',
    ' .. .... XXXXXooXoXXOoXXXXXXXXXXXXXXXXXX ...... ',
    ' .. .... XXXXooXXooOooXXXXXXXXXXXXXXXXXX ...... ',
    ' .. .... XXXXoXXOOoXoXXXXXXXXXX+++++XXXX ...... ',
    ' .. .... XXXXoXOXXoXoXXXXXXXXXX+++++XXXX ...... ',
    ' .. .. . XXXooOXXXXoXXXX+++++XX+++++XXXX ...... ',
    ' .. .... XXOoXXXXXXXXXXX+++++XX+++++XXXX ...... ',
    ' .. .... XOoXXXXX+++++XX+++++XX+++++XXXX ...... ',
    ' .. .... XXoXXXXX+++++XX+++++XX+++++XXXX ...... ',
    ' ....... XooXXXXX+++++XX+++++XX+++++XXXX ...... ',
    ' ..... . XXXXXXXX+++++XX+++++XX+++++XXXX ...... ',
    ' .......                                 ...... ',
    ' .............................................. ',
    ' ........ .... .... .... .... .... .... ....... ',
    ' .............................................. ',
    ' ..............                    ............ ',
    ' .............................................. ',
    ' .............................................. ',
    '                                                ',
    ]


class IPlot(QMainWindow):
    """A QMainWindow widget with a Plot widget as central widget.

    It provides:
    (1) a toolbar for printing and piping into Grace.
    (2) a legend with control to toggle curves between hidden and shown.
    (3) mouse tracking to display the coordinates in the status bar.
    (4) an infinite stack of zoom region.
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
        graceButton.setPixmap(QPixmap(grace_xpm))
        self.toolBar.addSeparator()

        mouseComboBox = QComboBox(self.toolBar)
        for name in ('3 buttons (PyQwt)',
                     '1 button',
                     '2 buttons',
                     '3 buttons (Qwt)'):
            mouseComboBox.insertItem(name)
        mouseComboBox.setCurrentItem(self.getZoomerMouseEventSet())
        self.toolBar.addSeparator()
        
        QWhatsThis.whatsThisButton(self.toolBar)

        self.connect(printButton, SIGNAL('clicked()'), self.printPlot)
        self.connect(graceButton, SIGNAL('clicked()'), self.gracePlot)
        self.connect(mouseComboBox, SIGNAL('activated(int)'),
                     self.setZoomerMouseEventSet)

        self.statusBar().message("Move the mouse within the plot canvas"
                                 " to show the cursor position.")
        self.__plot.canvas().setMouseTracking(1)
        self.connect(self.__plot, SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                     self.onMouseMoved)

        QWhatsThis.add(printButton,
                       'Print to a printer or an (E)PS file.')

        QWhatsThis.add(graceButton,
                       'Clone the plot into Grace.\n\n'
                       'The hardcopy output of Grace is better for\n'
                       'scientific journals and LaTeX documents.')
        
        QWhatsThis.add(
            mouseComboBox,
            'Configure the mouse events for the QwtPlotZoomer.\n\n'
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

        QWhatsThis.add(self.__plot.legend(),
                       'Clicking on a legend button toggles\n'
                       'a curve between hidden and shown.')

        QWhatsThis.add(
            self.__plot.canvas(),
            'Clicking on a legend button toggles a curve\n'
            'between hidden and shown.\n\n'
            'A QwtPlotZoomer lets you zoom infinitely deep\n'
            'by saving the zoom states on a stack. You can:\n'
            '- select a zoom region\n'
            '- unzoom all\n'
            '- walk down the stack\n'
            '- walk up the stack.\n\n'
            'The combo box in the toolbar lets you attach\n'
            'different sets of mouse events to those actions.'
            )

        self.resize(700, 500)
        self.show()

    # __init__()

    def printPlot(self):
        try:
            p = QPrinter(QPrinter.HighResolution)
        except AttributeError:
            p = QPrinter()
        p.setColorMode(QPrinter.Color)
        p.setOutputToFile(True)
        if p.setup():
            self.__plot.printPlot(p)

    # printPlot()

    def onMouseMoved(self, e):
        self.statusBar().message(
            ' -- '.join(self.formatCoordinates(e.pos().x(), e.pos().y())))

    # onMouseMoved()
        
    def __getattr__(self, attr):
        """Inherit everything from QMainWindow and Plot
        """
        if hasattr(QMainWindow, attr):
            return getattr(self.sipThis, attr)
        elif hasattr(self.__plot, attr):
            return getattr(self.__plot, attr)
        else:
            raise AttributeError, ('%s has no attribute named %s'
                                   % (self.__class__.__name__, attr))

    # __getattr__()

# class IPlot
        
        
# Admire!
from Numeric import *
import random

def testPlot():
    x = arange(-2*pi, 2*pi, 0.01)
    p = Plot(Curve(x, cos(x), Pen(Magenta, 2), "cos(x)"),
             Axis(Bottom, "linear x-axis"),
             Axis(Left, "linear y-axis"),
             Axis(Right, Logarithmic, "logarithmic y axis"),             
             Curve(x, exp(x), Pen(Red), "exp(x)", Right),
             ("PyQwt demo based on Qwt-%s (http://qwt.sf.net)"
              % QWT_VERSION_STR))
    x = x[0:-1:10]
    p.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),
           Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))
    return p


def testIPlot():
    x = arange(-2*pi, 2*pi, 0.01)
    p = IPlot(Curve(x, cos(x), Pen(Magenta, 2), "cos(x)"),
              Axis(Bottom, "linear x-axis"),
              Axis(Left, "linear y-axis"),
              Axis(Right, Logarithmic, "logarithmic y-axis"),
              Curve(x, exp(x), Pen(Red), "exp(x)", Right),
              ("PyQwt demo based on Qwt-%s (http://qwt.sf.net)"
               % QWT_VERSION_STR))
    x = x[0:-1:10]
    p.plot(Curve(x, cos(x-pi/4), Symbol(Circle, Yellow), "circle"),
           Curve(x, cos(x+pi/4), Pen(Blue), Symbol(Square, Cyan), "square"))
    return p


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
        
        
def testStandardMap():
    x = random.random()
    y = random.random()
    kappa = random.random()
    print "x = %s, y = %s, kappa = %s" % (x, y, kappa)
    xs, ys = standard_map(x, y, kappa, 1 << 16)
    p = IPlot(Curve(xs, ys, Symbol(Circle, Red), "standard_map"),
              ("PyQwt demo based on Qwt-%s (http://qwt.sf.net)"
               % QWT_VERSION_STR))
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

    
