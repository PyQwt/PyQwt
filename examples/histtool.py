#!/usr/bin/env python

# Interactive histogram resampling tool. Left-click to select bins you want
# to aggregate, then use popup menu to make aggregation. The cyan dotted line
# shows the total number of elements in selected bins. To make a selection the
# click must occur within histogram segments, to unselect click outside the
# histogram

# This version is a complete rewrite of the old one, now the application is
# written using Model View Controller paradigm, so I hope the code is more
# clean now.

# Copyright 2002: Serge Boiko <serge.boiko@gmx.net>

__version__ = 0.4
__date__ = "Wed Mar 19 12:47:09 2003"


import sys
from qt import *
from qwt import *
from Numeric import *
from MLab import *
import copy



# some utility functions
def find(a, cond):
    "Matlab's find equivalent"
    els = compress(cond, a, 0)
    ind = nonzero(cond)
    return (ind, els)

def histogram(a, bins):
    "Simple histogram tool"
    n = searchsorted(sort(a), bins)
    n = concatenate([n, [len(a)]])
    
    # sometimes i need average values too
    mean_val = zeros(len(bins), Float)
    for i in range(0, len(bins)-1):
        (ind, el) = find(a, (a >= bins[i])&(a<bins[i + 1]))
        try:
            mean_val[i] = mean(el)
        except ZeroDivisionError:
            mean_val[i] = bins[i]

    nums = n[1:]-n[:-1]
    # last elements are thrown away!
    return (nums[:-1], mean_val[:-1])

#----------------------------------------------------------------------
class HistogramWidget(QWidget):
    "Controller class"
    def __init__(self, data, bins, *args):
        "Data is the data we want to histogram"
        apply(QWidget.__init__, (self,) + args)
        self.selSegms = []
        self.model = HistogramModel(data, bins)
        self.pop = HistogramPopup(self)
        self.pop.insertItem("Aggregate Selection", self.makeAggregation)
        self.pop.insertSeparator()
        self.pop.insertItem("Undo!", self.makeUndo)
        self.pop.setItemEnabled(self.pop.idAt(2), 0)
        tt_txt = \
        """<p><b>Left-click</b> to select the bins you want 
        to aggregate. The cyan dotted 
        line shows the total number of elements 
        in the selected bins. To make a selection
        click within the histogram
        segments, to unselect click outside the
        histogram. <br><b>Right-click</b> shows the popup menu
        from which you can choose <b>"Aggregate Selection"</b>
        and <b>"Undo!"</b> actions</p>"""
     
        self.plot = HistogramPlot('Interactive Histogram Resampler', self)
        self.plot.setMinimumSize(300, 300)
        QToolTip.add(self, tt_txt)
        QObject.connect(self.model.emitter, PYSIGNAL("sendXYN"),
                        self.plot.drawHistogram)
        QObject.connect(self.plot, SIGNAL("plotMousePressed(const QMouseEvent&)"), 
                        self.slotMousePressed)
        QObject.connect(self.model.emitter, PYSIGNAL("sigClearSelection"), 
                       self.slotClearSelection)
        QObject.connect(self.plot, SIGNAL('plotMousePressed(const QMouseEvent&)'),
                        self.pop.raisePop)
        self.model.notifyUpdate()

    def whereIam(self, xPos, yPos):
        """If the mouse click occurs inside a histogram segment, returns
        the number of this segment (starting of course from zero), if
        the click occurs outside a histogram returns None"""
        # translate click's coordinate into plots's coordinates
        xPosTr = self.plot.invTransform(QwtPlot.xBottom, xPos)
        yPosTr = self.plot.invTransform(QwtPlot.yLeft, yPos)
        # which elements are to the right
        (ind, els) = find(self.model.bins, xPosTr <= self.model.bins)
        if (len(ind) == len(self.model.bins)) or (len(ind) == 0):
            # we missed
            pass
        else:
            pos = min(ind) - 1
            if (yPosTr >= 0) and (yPosTr <= self.model.nums[pos]):
                # we are inside a segment
                return pos
            else:
                return None

    def slotMousePressed(self, e):
        "Mouse press processing instructions go here"
        if e.button() == QMouseEvent.LeftButton:
            self.xPos = e.pos().x()
            self.yPos = e.pos().y()
            pos = self.whereIam(self.xPos, self.yPos)
            if pos is not None:
                self.selSegms.append(pos)
                sortSelSegms = sort(self.selSegms)
                for i in range(min(sortSelSegms), max(sortSelSegms) + 1, 1):
                    self.plot.setCurvePen(self.plot.curb[i], QPen(Qt.red, 2))
                    self.plot.replot()
                self.selSegms = range(min(sortSelSegms), max(sortSelSegms) + 1, 1)
                # total number of elms in selection
                tnums = sum(self.model.nums[min(self.selSegms):max(self.selSegms) + 1])
                self.plot.setCurvePen(self.plot.levelLine, QPen(Qt.darkCyan, 1, Qt.DotLine))
                # get axis bounds
                scD = self.plot.axisScale(QwtPlot.xBottom)
                self.plot.setCurveData(
                    self.plot.levelLine, [scD.lBound(), scD.hBound()], [tnums, tnums])
                self.plot.replot()
            else:
                for i in self.selSegms:
                    self.plot.setCurvePen(self.plot.curb[i], QPen(Qt.yellow, 2))
                    self.selSegms = []
                    self.plot.setCurveData(
                    self.plot.levelLine, [min(self.model.bins), max(self.model.bins)],
                    [0., 0.])
                    # "hide" the level line
                    self.plot.setCurvePen(self.plot.levelLine, QPen(Qt.yellow, 2))
                    self.plot.replot()
        else:
            pass
        
    def makeAggregation(self):
        "Say the model to aggregate segments"
        self.model.aggregateSegms(self.selSegms)
        self.pop.setItemEnabled(self.pop.idAt(2), 1)
        
    def makeUndo(self):
        self.model.undoSelection()
        self.plot.setCurveData(
            self.plot.levelLine, [min(self.model.bins), max(self.model.bins)],
            [0., 0.])
        # "hide" the level line
        self.plot.setCurvePen(self.plot.levelLine, QPen(Qt.yellow, 2))
        self.plot.replot()
        self.pop.setItemEnabled(self.pop.idAt(2), 0)
        
    def slotClearSelection(self):
        "Clear selected segments"
        self.selSegms = []


    def resizeEvent(self, e):
        self.plot.resize(e.size())
        self.plot.move(0,0)
#----------------------------------------------------------------------
class HistogramPlot(QwtPlot):
    """
    View class. Responsible for drawing the histogram. Extends
    QwtPlot.
    """
    def __init__(self, *args):
        apply(QwtPlot.__init__, (self, ) + args)
        self.setCanvasBackground(QColor(45, 48, 97))
        # calculate a histogram here
        self.setAxisAutoScale(HistogramPlot.yLeft)
        self.setAxisAutoScale(QwtPlot.xBottom)
        # set axis titles
        self.setAxisTitle(QwtPlot.xBottom, 'x -->')
        self.setAxisTitle(QwtPlot.yLeft, 'N -->')
        # disable the legend
        self.enableLegend(0)
        
    def drawHistogram(self, dataX, dataY, nums):
        "Draw histogram"
        self.removeCurves()
        # insert curves:
        self.curb = []
        for i in range(0, len(nums)):
            self.curb.append(self.insertCurve(str(i)))
            self.setCurvePen(self.curb[i], QPen(Qt.yellow, 2))
            self.setCurveData(self.curb[i], dataX[i, :], dataY[i, :])
            # draw a level line to show the num of elms in selection
            self.levelLine = self.insertCurve("LevelLine")
            self.setCurvePen(self.levelLine, QPen(Qt.yellow, 2))     
        self.replot()

#----------------------------------------------------------------------
class HistogramModel:
    """
    Store information about histogram segments and
    methods to work on them
    """
    def __init__(self, data, bins, *args):
        self.bins = bins
        self.data = data
        self.undo = UndoHolder(None, None)        
        (self.nums, mean_vals) = histogram(data, bins)
        (self.dataX, self.dataY) = self.makeCurveData(self.bins, self.nums)
        self.emitter = QObject()
        self.notifyUpdate()
        
    def makeCurveData(self, bins, nums):
        "Calculate points to be plotted as a histogram"
        dX = zeros((len(nums), 5), Float)
        dY = zeros((len(nums), 5), Float)
        for i in range(0, len(nums)):
            dX[i, :] = array([bins[i], bins[i], bins[i + 1], bins[i + 1], bins[i]])
            dY[i, :] = array([0., nums[i], nums[i], 0., 0.])
        return (dX, dY)  

    def notifyUpdate(self):
        "Send signal that data changed"
        self.emitter.emit(PYSIGNAL("sendXYN"),
                          (self.dataX, self.dataY, self.nums))
       
    def aggregateSegms(self, selSegms): 
        "Agregate segments on the histogram"
        # throw them away!
        self.undo.update(self.bins, self.data, self.nums)
        put(self.bins, selSegms[1:], -111.0)
        self.bins = compress(self.bins >= 0, self.bins)
        # calculate the total number of elements in selected bins
        tnums = sum(self.nums[min(selSegms):max(selSegms)+1])
        # throw them away!    
        put(self.nums, selSegms[1:], -111.0)
        self.nums = compress(self.nums >= 0, self.nums)
        (self.nums, self.mean_vals) = histogram(self.data, self.bins)
        (self.dataX, self.dataY)=self.makeCurveData(self.bins, self.nums)
        self.notifyUpdate()
        self.emitter.emit(PYSIGNAL("sigClearSelection"), ())
        
    def undoSelection(self):
        "Undo last changes"
        if self.undo.prevBins is not None:
            self.bins = self.undo.prevBins
        self.nums = self.undo.prevNums
        self.emitter.emit(PYSIGNAL("sigClearSelection"), ())
        (self.nums, mean_vals) = histogram(self.data, self.bins)
        (self.dataX, self.dataY) = self.makeCurveData(self.bins, self.nums)
        self.notifyUpdate()
        
#----------------------------------------------------------------------
class UndoHolder:
    "Stores information about previous state of the histogram"
    def __init__(self, bins, nums):
        "Constructs a holder to keep previous state"
        self.prevBins = copy.copy(bins)
        self.prevNums = copy.copy(nums)

    def update(self, newBins, newData, newNums):
        "Update the state of holder"
        self.prevBins = copy.copy(newBins)
        self.prevNums = copy.copy(newNums)

#----------------------------------------------------------------------
class HistogramPopup(QPopupMenu):
    def __init__(self, *args):
        apply(QPopupMenu.__init__, (self, ) + args)

    def raisePop(self, evt):
        """Raise popup only if right mouse pressed"""
        if evt.button() == QMouseEvent.RightButton:
            # we need to use global position here!
            self.popup(evt.globalPos())

#----------------------------------------------------------------------
# admire:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = rand(30)*10.
    bins = arange(0, 10.5, .5)
    demo = HistogramWidget(data, bins)
    app.setMainWidget(demo)
    demo.show()
    app.exec_loop()






