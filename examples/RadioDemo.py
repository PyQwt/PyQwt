#!/usr/bin/env python

# The Python version of qwt-*/examples/radio/radio.cpp

import sys
from qt import *
from qwt import *
from math import *


class TunerFrame(QFrame):

    def __init__(self, *args):
        apply(QFrame.__init__, (self,) + args)

        self.setFixedSize(720, 120)

        lblTune = QLabel("Tuning", self)
        lblTune.setGeometry(30, 100, 90, 15)
        lblTune.setAlignment(Qt.AlignCenter)

        self.sldFreq = QwtSlider(self, "", Qt.Horizontal, QwtSlider.Top)
        self.sldFreq.setGeometry(30, 10, 660, 60)
        self.sldFreq.setScaleMaxMinor(5)
        self.sldFreq.setScaleMaxMajor(12)
        self.sldFreq.setThumbLength(80)
        self.sldFreq.setBorderWidth(1)
        self.sldFreq.setRange(87.5, 108, 0.01, 10)

        self.whlFreq = QwtWheel(self)
        self.whlFreq.setGeometry(540, 80, 150, 30)
        self.whlFreq.setMass(0.5)
        self.whlFreq.setRange(87.5, 108, 0.01)
        self.whlFreq.setTotalAngle(3600.0)

        self.thmTune = QwtThermo(self)
        self.thmTune.setGeometry(30, 80, 90, 20)
        self.thmTune.setOrientation(Qt.Horizontal, QwtThermo.None)
        self.thmTune.setRange(0.0, 1.0)
        self.thmTune.setFillColor(Qt.green)

        self.connect(self.whlFreq, SIGNAL("valueChanged(double)"),
                     self.adjustFreq)
        self.connect(self.sldFreq, SIGNAL("valueChanged(double)"),
                     self.adjustFreq)

    def adjustFreq(self, f):
        factor = 13.0 / (108 - 87.5)
        x = (f - 87.5)  * factor
        field = (sin(x) * cos(4.0 * x))**2
        self.thmTune.setValue(field)  
        if self.sldFreq.value() != f:
            self.sldFreq.setValue(f)
        if self.whlFreq.value() != f:
            self.whlFreq.setValue(f)
        self.emit(PYSIGNAL("fieldChanged(double)"), (field,))	

    def setFreq(self, f):
        self.whlFreq.setValue(f)


class AmplifierFrame(QFrame):

    def __init__(self, *args):
        apply(QFrame.__init__, (self,) + args)

        self.phs = 0.0
        self.setFont(QFont("Helvetica", 10, QFont.Bold))

        # FIXME: to make the QwtKnob's display self.knob is needed. Why
        self.knbVolume = QwtKnob(self)
        self.knbBass = QwtKnob(self)
        self.knbBalance = QwtKnob(self)
        self.knbTreble = QwtKnob(self)

        lblVolume = QLabel("Volume", self)
        lblTreble = QLabel("Treble", self)
        lblBass = QLabel("Bass", self)
        lblBalance = QLabel("Balance", self)

        self.knbVolume.setRange(0.0, 10, 0.1)
        self.knbBalance.setRange(-10.0, 10.0, 0.1)
        self.knbBalance.setScaleMaxMajor(10)
        self.knbTreble.setRange(-10.0, 10.0, 0.1)
        self.knbTreble.setScaleMaxMajor(10)
        self.knbBass.setRange(-10.0, 10.0,0.1)
        self.knbBass.setScaleMaxMajor(10)
    
        self.knbVolume.setGeometry(20, 10, 100, 100)
        self.knbVolume.setValue(2.0)
        lblVolume.setGeometry(20, 100, 100, 15)
        lblVolume.setAlignment(Qt.AlignCenter)
        self.knbVolume.setScaleMaxMajor(10)
    
        self.knbBalance.setGeometry(140, 10, 100, 100)
        lblBalance.setGeometry(140, 100, 100, 15)
        lblBalance.setAlignment(Qt.AlignCenter)

        self.knbTreble.setGeometry(260, 10, 100, 100)
        lblTreble.setGeometry(260, 100, 100, 15)
        lblTreble.setAlignment(Qt.AlignCenter)

        self.knbBass.setGeometry(380, 10, 100, 100)
        lblBass.setGeometry(380, 100, 100, 15)
        lblBass.setAlignment(Qt.AlignCenter)

        lblLeft = QLabel("Left [dB]", self)
        lblRight = QLabel("Right [dB]", self)
    
        self.thmLeft = QwtThermo(self)
        self.thmRight = QwtThermo(self)

        self.thmLeft.setGeometry(540, 10, 60, 90)
        self.thmLeft.setPipeWidth(6)
        self.thmLeft.setRange(-40, 10)
        self.thmLeft.setFillColor(Qt.green)
        self.thmLeft.setAlarmColor(Qt.red)
        self.thmLeft.setAlarmLevel(0.0)
        self.thmLeft.setAlarmEnabled(1)
    
        self.thmRight.setGeometry(610, 10, 60, 90)
        self.thmRight.setPipeWidth(6)
        self.thmRight.setRange(-40, 10)
        self.thmRight.setFillColor(Qt.green)
        self.thmRight.setAlarmColor(Qt.red)
        self.thmRight.setAlarmLevel(0.0)
        self.thmRight.setAlarmEnabled(1)
    
        lblLeft.setGeometry(550,100, 60,15)
        lblRight.setGeometry(620,100,60,15)
    
        self.setFixedSize(720, 120)
        tid = self.startTimer(50)

    def timerEvent(self, e):
        sig_bass = (1.0 + 0.1*self.knbBass.value()) * sin(13.0*self.phs)
        sig_mid_l = sin(17.0*self.phs)
        sig_mid_r = cos(17.5*self.phs)
        sig_trbl_l = 0.5*(1.0+0.1*self.knbTreble.value()) * sin(35.0*self.phs)
        sig_trbl_r = 0.5*(1.0+0.1*self.knbTreble.value()) * sin(34.0*self.phs)
        sig_l = 0.05*self.master*self.knbVolume.value() * \
                (sig_bass+sig_mid_l+sig_trbl_l)**2
        sig_r = 0.05*self.master*self.knbVolume.value() * \
                (sig_bass+sig_mid_r+sig_trbl_r)**2
    
        balance = 0.1 * self.knbBalance.value() 
        if balance > 0: 
            sig_l *= (1.0 - balance)
        else:
            sig_r *= (1.0 + balance)

        if sig_l > 0.01:
            sig_l = 20.0 * log10(sig_l)
        else:
            sig_l = -40.0

        if sig_r > 0.01:
            sig_r = 20.0 * log10(sig_r)
        else:
            sig_r = - 40.0
        self.thmLeft.setValue(sig_l)
        self.thmRight.setValue(sig_r)

        self.phs += pi / 100
        if self.phs > pi:
            self.phs = 0

    
    def setMaster(self, v):
        self.master = v


class RadioDemo(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        self.tuner = TunerFrame(self)
        self.tuner.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.amplifier = AmplifierFrame(self)
        self.amplifier.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setFixedSize(720, 240)

        self.tuner.move(0, 0)
        self.amplifier.move(0, 120)
    
        self.connect(self.amplifier, PYSIGNAL("fieldChanged(double)"),
                     self.amplifier.setMaster)

        self.amplifier.setMaster(1.0)
        self.tuner.setFreq(90.0)


def make():
    demo = RadioDemo()
    demo.show()
    return demo

def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# Admire!
if __name__ == '__main__':
    main(sys.argv)


