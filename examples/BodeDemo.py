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

        self.setTitle('Frequency Response of a Second-Order System');

        self.setCanvasBackground(Qt.darkBlue)

        # outline
        self.enableOutline(1)
        self.setOutlinePen(QPen(Qt.green))

        # legend
        self.setAutoLegend(1)
        self.enableLegend(1)
        self.setLegendPos(Qwt.Bottom)
        self.setLegendFrameStyle(QFrame.Box | QFrame.Sunken)

        # grid 
        self.enableGridXMin()
        self.setGridMajPen(QPen(Qt.white, 0, Qt.DotLine));
        self.setGridMinPen(QPen(Qt.gray, 0 , Qt.DotLine));

        # axes
        self.enableAxis(QwtPlot.yRight);
        self.setAxisTitle(QwtPlot.xBottom, 'Normalized Frequency');
        self.setAxisTitle(QwtPlot.yLeft, 'Amplitude [dB]');
        self.setAxisTitle(QwtPlot.yRight, 'Phase [deg]');

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

        # marker
        self.mrk1 = self.insertMarker()
        self.setMarkerLineStyle(self.mrk1, QwtMarker.VLine)
        self.setMarkerPos(self.mrk1, 0.0, 0.0)
        self.setMarkerLabelAlign(self.mrk1, Qt.AlignRight | Qt.AlignBottom)
        self.setMarkerPen(self.mrk1, QPen(Qt.green, 0, Qt.DashDotLine))
        self.setMarkerFont(self.mrk1, QFont('Helvetica', 10, QFont.Bold))

        self.mrk2 = self.insertLineMarker('', QwtPlot.yLeft)
        self.setMarkerLabelAlign(self.mrk2, Qt.AlignRight | Qt.AlignBottom)
        self.setMarkerPen(self.mrk2, QPen(
            QColor(200, 150, 0), 0, Qt.DashDotLine))
        self.setMarkerFont(self.mrk2, QFont('Helvetica', 10, QFont.Bold))
        self.setMarkerSymbol(self.mrk2, QwtSymbol(
            QwtSymbol.Diamond, QBrush(Qt.yellow), QPen(Qt.green), QSize(7,7)))

        self.setDamp(0.01)
            

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
        self.setMarkerLabel(self.mrk1, '-3 dB at f %4g' % f3)
        imax = argmax(a)
        self.setMarkerPos(self.mrk2, f[imax], a[imax]);
        self.setMarkerLabel(self.mrk2, 'Peak: %4g dB' % a[imax])

        self.replot()



zoomInfo = 'Zoom: Press mouse button and drag'
cursorInfo = 'Cursor Pos: Press mouse button in plot region'

class BodeDemo(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)

        self.zoomState = 0
        
        self.plot = BodePlot(self)
        self.plot.setMargin(5)
        self.setCentralWidget(self.plot)

        self.toolBar = QToolBar(self)

        btnZoom = QToolButton(self.toolBar)
        btnZoom.setTextLabel("Zoom")
        btnZoom.setPixmap(QPixmap(zoom_xpm))
        btnZoom.setToggleButton(1)
        btnZoom.setUsesTextLabel(1)

        btnPrint = QToolButton(self.toolBar)
        btnPrint.setTextLabel("Print")
        btnPrint.setPixmap(QPixmap(print_xpm))
        btnPrint.setUsesTextLabel(1)

        self.toolBar.setStretchableWidget(QWidget(self.toolBar))
        dampBox = QHBox(self.toolBar)
        dampBox.setSpacing(10)
        QLabel("Damping Factor", dampBox)
        self.cntDamp = QwtCounter(dampBox)
        self.cntDamp.setRange(0.01, 5.0, 0.01)
        self.cntDamp.setValue(0.01)
    
        #self.toolBar(self.toolBar)
        self.statusBar()

        self.showInfo(cursorInfo)
        
        QObject.connect(self.cntDamp, SIGNAL('valueChanged(double)'),
                        self.plot.setDamp)
        QObject.connect(btnPrint, SIGNAL('clicked()'), self.printPlot)
        QObject.connect(btnZoom, SIGNAL('toggled(bool)'), self.zoom)
        QObject.connect(self.plot,
                        SIGNAL('plotMouseMoved(const QMouseEvent&)'),
                        self.plotMouseMoved)
        QObject.connect(self.plot,
                        SIGNAL('plotMousePressed(const QMouseEvent&)'),
                        self.plotMousePressed)
        QObject.connect(self.plot,
                        SIGNAL('plotMouseReleased(const QMouseEvent&)'),
                        self.plotMouseReleased)

    def printPlot(self):
        p = QPrinter()
        if p.setup():
            self.plot.printPlot(p);

    def zoom(self, on):
        if on:
            self.zoomState = 1
        else:
            self.plot.setAxisAutoScale(QwtPlot.yLeft)
            self.plot.setAxisAutoScale(QwtPlot.yRight)
            self.plot.setAxisAutoScale(QwtPlot.xBottom)
            self.plot.replot()
            self.zoomState = 0
        if self.zoomState:
            self.showInfo(zoomInfo)
        else:
            self.showInfo(cursorInfo)

    def showInfo(self, text):
        self.statusBar().message(text)
        
    def plotMouseMoved(self, e):
        frequency = self.plot.invTransform(QwtPlot.xBottom, e.pos().x())
        amplitude = self.plot.invTransform(QwtPlot.yLeft, e.pos().y())
        phase = self.plot.invTransform(QwtPlot.yRight, e.pos().y())
        self.showInfo('Freq=%g, Ampl=%g, Phase=%g' %
                      (frequency, amplitude, phase))
        
    def plotMousePressed(self, e):
        # Python semantics: self.pos = e.pos() does not work; force a copy
        self.xpos = e.pos().x()
        self.ypos = e.pos().y()
        self.plotMouseMoved(e)  # fake a mouse move to show the cursor position
        if (self.zoomState):
            self.plot.setOutlineStyle(Qwt.Rect) 
        else:
            self.plot.setOutlineStyle(Qwt.Cross)

    def plotMouseReleased(self, e):
        if (self.zoomState):
            x1 = min(self.xpos, e.pos().x());
            x2 = max(self.xpos, e.pos().x());
            y1 = min(self.ypos, e.pos().y());
            y2 = max(self.ypos, e.pos().y());
            lim = 5 - (y2 - y1 + 1) / 2
            if lim > 0:
                y1 -= lim
                y2 += lim
            lim = 5 - (x2 - x1 + 1) / 2
            if lim > 0:
                x1 -= lim
                x2 += lim
            self.plot.setAxisScale(QwtPlot.yLeft,
                                   self.plot.invTransform(QwtPlot.yLeft, y1),
                                   self.plot.invTransform(QwtPlot.yLeft, y2))
            self.plot.setAxisScale(QwtPlot.yRight,
                                   self.plot.invTransform(QwtPlot.yRight, y1),
                                   self.plot.invTransform(QwtPlot.yRight, y2))
            self.plot.setAxisScale(QwtPlot.xBottom,
                                   self.plot.invTransform(QwtPlot.xBottom, x1),
                                   self.plot.invTransform(QwtPlot.xBottom, x2))
            self.plot.replot()
            self.showInfo(cursorInfo);
            self.plot.setOutlineStyle(Qwt.Triangle);
            self.zoomState = 0


def main(args):
    app = QApplication(args)
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
