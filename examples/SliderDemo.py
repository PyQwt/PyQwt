#!/usr/bin/env python

# an almost literal translation of qwt-*/examples/sliders/sliders.cpp

import sys
from qt import *
from qwt import *

class SliderDemo(QWidget):
    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        # make sliders
        sldV1 = QwtSlider(self, "", Qt.Vertical, QwtSlider.Left,
                          QwtSlider.BgSlot)
        sldV2 = QwtSlider(self, "", Qt.Vertical, QwtSlider.None,
                          QwtSlider.BgTrough)
        sldV3 = QwtSlider(self, "", Qt.Vertical, QwtSlider.Right,
                          QwtSlider.BgSlot | QwtSlider.BgTrough)
    
        sldH1 = QwtSlider(self, "", Qt.Horizontal, QwtSlider.Top,
                          QwtSlider.BgTrough)
        sldH2 = QwtSlider(self, "", Qt.Horizontal, QwtSlider.None,
			  QwtSlider.BgSlot | QwtSlider.BgTrough)
        sldH3 = QwtSlider(self, "", Qt.Horizontal,
                          QwtSlider.Bottom, QwtSlider.BgSlot)

        # slider properties
        sldV1.setRange(0.0, 100.0, 1.0, 5)
        sldV1.setScaleMaxMinor(5)

        sldV2.setRange(0.0, 100.0, 1.0, 10)

        sldV3.setThumbWidth(20)
        sldV3.setBorderWidth(1)
        sldV3.setRange(0.0, 4.0, 0.01)
        sldV3.setScale(1.0, 1.0e4, 1)
        sldV3.setScaleMaxMinor(10)
    
        sldH1.setThumbWidth(10)
        sldH1.setRange(-10.0, 10.0, 1.0, 0)

        sldH2.setRange(0.0, 1.0, 0.01, 5)

        sldH3.setRange(1000.0, 3000.0, 10.0, 10)
        sldH3.setThumbWidth(25)
        sldH3.setThumbLength(12)
        sldH3.setMargins(10, 0)

        lblV1 = QLabel("0", self)
        lblV2 = QLabel("0", self)
        self.lblV3 = QLabel("1.0", self)
        lblH1 = QLabel("0", self)
        lblH2 = QLabel("0.0", self)
        lblH3 = QLabel("0", self)

        lblHTitle = QLabel("Horizontal Sliders", self)
        lblVTitle = QLabel("Vertical Sliders", self)
        lblHTitle.setFont(QFont("Helvetica", 14, QFont.Bold))
        lblVTitle.setFont(QFont("Helvetica", 14, QFont.Bold))

        lytGrid = QGridLayout(self, 5, 5, 20, 10)

        lblHTitle.setMinimumSize(lblHTitle.sizeHint())
        lblVTitle.setMinimumSize(lblVTitle.sizeHint())
        lytGrid.addMultiCellWidget(lblVTitle, 0, 0, 0, 2)
        lytGrid.addMultiCellWidget(lblHTitle, 0, 0, 3, 4)

        sldV1.setMinimumSize(sldV1.sizeHint().width(), 100)
        sldV1.setMaximumSize(sldV1.sizeHint().width(), 1000)

        sldV2.setMinimumSize(20, 100)
        sldV2.setMaximumSize(20, 1000)
        
        sldV3.setMinimumSize(sldV3.sizeHint().width(), 100)
        sldV3.setMaximumSize(sldV3.sizeHint().width(), 1000)

        lytGrid.addMultiCellWidget(sldV1, 1, 3, 0, 0, Qt.AlignRight)
        lytGrid.addMultiCellWidget(sldV2, 1, 3, 1, 1, Qt.AlignHCenter)
        lytGrid.addMultiCellWidget(sldV3, 1, 3, 2, 2, Qt.AlignLeft)

        sldH1.setMaximumSize(1000, sldH1.sizeHint().height())
        sldH1.setMinimumSize(150, sldH1.sizeHint().height())

        sldH2.setMinimumSize(150, 20)
        sldH2.setMaximumSize(1000, 20)

        sldH3.setMinimumSize(150, sldH3.sizeHint().height())
        sldH3.setMaximumSize(1000, sldH3.sizeHint().height())
    
        lytGrid.addWidget(sldH1, 1, 3, Qt.AlignTop)
        lytGrid.addWidget(sldH2, 2, 3, Qt.AlignVCenter)
        lytGrid.addWidget(sldH3, 3, 3, Qt.AlignBottom)

        lblV1.setFixedSize(60, 30)
        lblV1.setAlignment(Qt.AlignHCenter)
        lblV2.setFixedSize(60, 30)
        lblV2.setAlignment(Qt.AlignHCenter)
        self.lblV3.setFixedSize(60, 30)
        self.lblV3.setAlignment(Qt.AlignLeft)
    
        lytGrid.addWidget(lblV1, 4, 0, Qt.AlignRight)
        lytGrid.addWidget(lblV2, 4, 1, Qt.AlignHCenter)
        lytGrid.addWidget(self.lblV3, 4, 2, Qt.AlignLeft)

        lblH1.setFixedSize(50, 30)
        lblH1.setAlignment(Qt.AlignVCenter)
        lblH2.setFixedSize(50, 30)
        lblH2.setAlignment(Qt.AlignVCenter)
        lblH3.setFixedSize(50, 30)
        lblH3.setAlignment(Qt.AlignVCenter)

        lytGrid.addWidget(lblH1, 1, 4, Qt.AlignVCenter)
        lytGrid.addWidget(lblH2, 2, 4, Qt.AlignVCenter)
        lytGrid.addWidget(lblH3, 3, 4, Qt.AlignVCenter)

        lytGrid.setColStretch(0,  1)
        lytGrid.setColStretch(1,  3)
        lytGrid.setColStretch(2,  1)
        lytGrid.setColStretch(3, 10)
        lytGrid.setColStretch(4,  0)

        lytGrid.setRowStretch(0,  1)
        lytGrid.setRowStretch(1,  3)
        lytGrid.setRowStretch(2, 10)
        lytGrid.setRowStretch(3,  3)
        lytGrid.setRowStretch(4,  0)
   
        QObject.connect(sldH1, SIGNAL("valueChanged(double)"), lblH1.setNum)
        QObject.connect(sldH2, SIGNAL("valueChanged(double)"), lblH2.setNum)
        QObject.connect(sldH3, SIGNAL("valueChanged(double)"), lblH3.setNum)
        QObject.connect(sldV1, SIGNAL("valueChanged(double)"), lblV1.setNum)
        QObject.connect(sldV2, SIGNAL("valueChanged(double)"), lblV2.setNum)
        QObject.connect(sldV3, SIGNAL("valueChanged(double)"), self.setV3)
        
        self.setMinimumSize(550, 250)

    def setV3(self, value):
        self.lblV3.setNum(10.0**value)


def make():
    demo = SliderDemo()
    demo.show()
    return demo

def main(args):
    app = QApplication(sys.argv)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# Admire!
if __name__ == '__main__':
    main(sys.argv)
