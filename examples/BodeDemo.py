#!/usr/bin/env python

# The Python version of qwt-*/examples/bode/bode.cpp

# To get an impression of the expressive power of Numeric,
# compare the Python and C++ versions of recalc()

import sys
from qt import *
from qwt import *
from Numeric import *

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

zoom_xpm = ['32 32 8 1',
            '# c #000000',
            'b c #c0c0c0',
            'a c #ffffff',
            'e c #585858',
            'd c #a0a0a4',
            'c c #0000ff',
            'f c #00ffff',
            '. c None',
            '..######################........',
            '.#a#baaaaaaaaaaaaaaaaaa#........',
            '#aa#baaaaaaaaaaaaaccaca#........',
            '####baaaaaaaaaaaaaaaaca####.....',
            '#bbbbaaaaaaaaaaaacccaaa#da#.....',
            '#aaaaaaaaaaaaaaaacccaca#da#.....',
            '#aaaaaaaaaaaaaaaaaccaca#da#.....',
            '#aaaaaaaaaabe###ebaaaaa#da#.....',
            '#aaaaaaaaa#########aaaa#da#.....',
            '#aaaaaaaa###dbbbb###aaa#da#.....',
            '#aaaaaaa###aaaaffb###aa#da#.....',
            '#aaaaaab##aaccaaafb##ba#da#.....',
            '#aaaaaae#daaccaccaad#ea#da#.....',
            '#aaaaaa##aaaaaaccaab##a#da#.....',
            '#aaaaaa##aacccaaaaab##a#da#.....',
            '#aaaaaa##aaccccaccab##a#da#.....',
            '#aaaaaae#daccccaccad#ea#da#.....',
            '#aaaaaab##aacccaaaa##da#da#.....',
            '#aaccacd###aaaaaaa###da#da#.....',
            '#aaaaacad###daaad#####a#da#.....',
            '#acccaaaad##########da##da#.....',
            '#acccacaaadde###edd#eda#da#.....',
            '#aaccacaaaabdddddbdd#eda#a#.....',
            '#aaaaaaaaaaaaaaaaaadd#eda##.....',
            '#aaaaaaaaaaaaaaaaaaadd#eda#.....',
            '#aaaaaaaccacaaaaaaaaadd#eda#....',
            '#aaaaaaaaaacaaaaaaaaaad##eda#...',
            '#aaaaaacccaaaaaaaaaaaaa#d#eda#..',
            '########################dd#eda#.',
            '...#dddddddddddddddddddddd##eda#',
            '...#aaaaaaaaaaaaaaaaaaaaaa#.####',
            '...########################..##.']


class BodePlot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        self.setTitle('Frequency Response of a 2<sup>nd</sup>-order System')
        self.setCanvasBackground(Qt.darkBlue)

        # legend
        self.setAutoLegend(True)
        self.enableLegend(True)
        self.setLegendPos(Qwt.Bottom)
        self.setLegendFrameStyle(QFrame.Box | QFrame.Sunken)

        # grid 
        self.enableGridXMin()
        self.setGridMajPen(QPen(Qt.white, 0, Qt.DotLine));
        self.setGridMinPen(QPen(Qt.gray, 0 , Qt.DotLine));

        # axes
        self.enableAxis(QwtPlot.yRight);
        self.setAxisTitle(QwtPlot.xBottom, u'\u03c9/\u03c9<sub>0</sub>')
        self.setAxisTitle(QwtPlot.yLeft, 'Amplitude [dB]')
        self.setAxisTitle(QwtPlot.yRight, u'Phase [\u00b0]')

        self.setAxisOptions(QwtPlot.xBottom, QwtAutoScale.Logarithmic);
        self.setAxisMaxMajor(QwtPlot.xBottom, 6);
        self.setAxisMaxMinor(QwtPlot.xBottom, 10);

        # curves
        self.curve1 = self.insertCurve('Amplitude')
        self.setCurvePen(self.curve1, QPen(Qt.yellow))
        self.setCurveYAxis(self.curve1, QwtPlot.yLeft)
        
        self.curve2 = self.insertCurve('Phase')
        self.setCurvePen(self.curve2, QPen(Qt.cyan))
        self.setCurveYAxis(self.curve2, QwtPlot.yRight)

        # alias
        fn = self.fontInfo().family()

        # marker
        self.mrk1 = self.insertMarker()
        self.setMarkerLineStyle(self.mrk1, QwtMarker.VLine)
        self.setMarkerPos(self.mrk1, 0.0, 0.0)
        self.setMarkerLinePen(self.mrk1, QPen(Qt.green, 2, Qt.DashDotLine))
        self.setMarkerLabelAlign(self.mrk1, Qt.AlignRight | Qt.AlignBottom)
        self.setMarkerLabel(self.mrk1, '', QFont(fn, 12, QFont.Bold),
                            Qt.green, QPen(Qt.NoPen), QBrush(Qt.red))

        self.mrk2 = self.insertLineMarker('', QwtPlot.yLeft)
        self.setMarkerLinePen(self.mrk2, QPen(Qt.red, 2, Qt.DashDotLine))
        self.setMarkerLabelAlign(self.mrk2, Qt.AlignRight | Qt.AlignBottom)
        self.setMarkerLabel(self.mrk2, '', QFont(fn, 12, QFont.Bold),
                            Qt.red, QPen(Qt.NoPen),
                            QBrush(self.canvasBackground()))
        self.setMarkerSymbol(self.mrk2, QwtSymbol(
            QwtSymbol.Diamond, QBrush(Qt.yellow), QPen(Qt.green), QSize(7,7)))

        # text marker
        m = self.insertMarker()
        self.setMarkerPos(m, 0.1, -20.0)
        self.setMarkerLabelAlign(m, Qt.AlignRight | Qt.AlignBottom)
        self.setMarkerLabel(
            m,
            QString(u'[1-(\u03c9/\u03c9<sub>0</sub>)<sup>2</sup>+2j\u03c9/Q]'
                    '<sup>-1</sup>'),
            QFont(fn, 12, QFont.Bold, False),
            Qt.blue, QPen(Qt.red, 2), QBrush(Qt.yellow))
        self.setDamp(0.01)

    # __init__()

    def setDamp(self, d):
        self.damping = d
        # Numerical Python: f, g, a and p are arrays!
        f = exp(log(10.0)*arrayrange(-2, 2.02, 0.04))
        g = 1.0/(1.0-f*f+2j*self.damping*f)
        a = 20.0*log10(abs(g))
        p = 180*arctan2(g.imag, g.real)/pi
        self.setCurveData(self.curve1, f, a)
        self.setCurveData(self.curve2, f, p)
        # show3dB and showPeak
        i3 = argmax(where(less(a, -3.0), a, -100.0))
        f3 = f[i3] - (a[i3]+3.0)*(f[i3]-f[i3-1])/(a[i3]-a[i3-1])
        self.setMarkerPos(self.mrk1, f3, 0.0)
        self.setMarkerLabelText(self.mrk1, '-3 dB at f = %4g' % f3)
        imax = argmax(a)
        self.setMarkerPos(self.mrk2, f[imax], a[imax]);
        self.setMarkerLabelText(self.mrk2, 'Peak: %4g dB' % a[imax])

        self.replot()

    # setDamp()

# class BodePlot


class BodeDemo(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)

        self.plot = BodePlot(self)
        self.plot.setMargin(5)

        self.zoomers = []
        zoomer = QwtPlotZoomer(QwtPlot.xBottom,
                               QwtPlot.yLeft,
                               QwtPicker.DragSelection,
                               QwtPicker.AlwaysOff,
                               self.plot.canvas())
        zoomer.setRubberBandPen(QPen(Qt.green))
        self.zoomers.append(zoomer)

        zoomer = QwtPlotZoomer(QwtPlot.xTop,
                               QwtPlot.yRight,
                               QwtPicker.DragSelection,
                               QwtPicker.AlwaysOff,
                               self.plot.canvas())
        zoomer.setRubberBand(QwtPicker.NoRubberBand)
        self.zoomers.append(zoomer)

        self.picker = QwtPlotPicker(
            QwtPlot.xBottom,
            QwtPlot.yLeft,
            QwtPicker.PointSelection | QwtPicker.DragSelection,
            QwtPlotPicker.CrossRubberBand,
            QwtPicker.AlwaysOff,
            self.plot.canvas())
        self.picker.setRubberBandPen(QPen(Qt.green))
 
        self.setCentralWidget(self.plot)

        self.toolBar = QToolBar(self)

        btnZoom = QToolButton(self.toolBar)
        btnZoom.setTextLabel("Zoom")
        btnZoom.setPixmap(QPixmap(zoom_xpm))
        btnZoom.setToggleButton(True)
        btnZoom.setUsesTextLabel(True)

        btnPrint = QToolButton(self.toolBar)
        btnPrint.setTextLabel("Print")
        btnPrint.setPixmap(QPixmap(print_xpm))
        btnPrint.setUsesTextLabel(True)

        self.toolBar.setStretchableWidget(QWidget(self.toolBar))
        dampBox = QHBox(self.toolBar)
        dampBox.setSpacing(10)
        QLabel("Damping Factor", dampBox)
        self.cntDamp = QwtCounter(dampBox)
        self.cntDamp.setRange(0.01, 5.0, 0.01)
        self.cntDamp.setValue(0.01)
    
        self.statusBar()
        self.zoom(False)
        
        self.connect(self.cntDamp, SIGNAL('valueChanged(double)'),
                     self.plot.setDamp)
        self.connect(btnPrint, SIGNAL('clicked()'),
                     self.printPlot)
        self.connect(btnZoom, SIGNAL('toggled(bool)'),
                     self.zoom)
        self.connect(self.picker, SIGNAL('moved(const QPoint &)'), self.moved)
        self.connect(self.picker, SIGNAL('selected(const QPointArray &)'),
                     self.selected)

    # __init__()

    def printPlot(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
        except AttributeError:
            printer = QPrinter()
        printer.setOrientation(QPrinter.Landscape)
        printer.setColorMode(QPrinter.Color)
        printer.setOutputToFile(True)
        printer.setOutputFileName('bode-example-%s.ps' % qVersion())
        if printer.setup():
            self.plot.printPlot(printer)

    # printPlot()
    
    def zoom(self, on):
        self.zoomers[0].setEnabled(on)
        self.zoomers[0].zoom(0)
        
        self.zoomers[1].setEnabled(on)
        self.zoomers[1].zoom(0)

        if on:
            self.picker.setRubberBand(QwtPicker.NoRubberBand)
        else:
            self.picker.setRubberBand(QwtPicker.CrossRubberBand)

        self.showInfo()

    # zoom()
    
    def moved(self, point):
        info = "Freq=%g, Ampl=%g, Phase=%g" % (
            self.plot.invTransform(QwtPlot.xBottom, point.x()),
            self.plot.invTransform(QwtPlot.yLeft, point.y()),
            self.plot.invTransform(QwtPlot.yRight, point.y()))
        self.showInfo(info)

    # moved()

    def selected(self, points):
        self.showInfo()

    # selected()

    def showInfo(self, text=None):
        if text:
            self.statusBar().message(text)
        elif self.picker.rubberBand():
            self.statusBar().message(
                'Cursor Pos: Press left mouse button in plot region')
        else:
            self.statusBar().message(
                'Zoom: Press mouse button and drag')
                
    # showInfo()
    
# class BodeDemo
    

def main(args):
    app = QApplication(args)
    fonts = QFontDatabase()
    if QString('Verdana') in fonts.families():
        app.setFont(QFont('Verdana'))
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()


def make():
    demo = BodeDemo()
    demo.resize(540, 400)
    demo.show()
    return demo
    
# Admire!
if __name__ == '__main__':
    main(sys.argv)
