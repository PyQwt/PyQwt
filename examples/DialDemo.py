#!/usr/bin/env python

import math
import random
import sys
from qt import *
from qwt import *

def enumColorGroups():
    """Masks the change in enum/int type checking new in SIP-4.2.x
    """
    if isinstance(int, QPalette.ColorGroup):
        return range(QPalette.NColorGroups)
    else:
        return [QPalette.ColorGroup(i)
                for i in range(QPalette.NColorGroups)
                ]

# enumColorRoles()

def enumColorRoles():
    """Masks the change in enum/int type checking new in SIP-4.2.x
    """
    if isinstance(int, QColorGroup.ColorRole):
        return range(QColorGroup.NColorRoles)
    else:
        return [QColorGroup.ColorRole(i)
                for i in range(QColorGroup.NColorRoles)
                ]

# enumColorRoles()

def enumHands():
    """Masks the change in enum/int type checking new in SIP-4.2.x
    """
    if isinstance(int, QwtAnalogClock.Hand):
        return range(QwtAnalogClock.NHands)
    else:
        return [QwtAnalogClock.Hand(i)
                for i in range(QwtAnalogClock.NHands)
                ]

# enumHands()


class CompassGrid(QGrid):

    def __init__(self, *args):
        QGrid.__init__(self, 3, *args)
        if qVersion() < '3.0.0':
            self.setPaletteBackgroundColor = self.setBackgroundColor
            self.paletteBackgroundColor = self.backgroundColor
        self.setPaletteBackgroundColor(Qt.gray)
        for pos in range(6):
            self.__createCompass(pos)
        layout = self.layout()
        for col in range(layout.numCols()):
            layout.setColStretch(col, 1)

    # __init__()
    
    def __createCompass(self, pos):
        colorGroup = QColorGroup()
        for cr in enumColorRoles():
            colorGroup.setColor(cr, QColor())

        colorGroup.setColor(
            QColorGroup.Base, self.paletteBackgroundColor().light(120))
        colorGroup.setColor(
            QColorGroup.Foreground, colorGroup.color(QColorGroup.Base))

        compass = QwtCompass(self)
        compass.setLineWidth(4)
        if pos < 3:
            compass.setFrameShadow(QwtCompass.Sunken)
        else:
            compass.setFrameShadow(QwtCompass.Raised)

        if pos == 0:
            compass.setMode(QwtCompass.RotateScale)
            rose = QwtSimpleCompassRose(16, 2)
            rose.setWidth(0.15)
            compass.setRose(rose)
        elif pos == 1:
            compass.setLabelMap({0.0: "N",
                                 90.0: "E",
                                 180.0: "S",
                                 270.0: "W"})
            rose = QwtSimpleCompassRose(4, 1)
            compass.setRose(rose)
            compass.setNeedle(QwtCompassWindArrow(QwtCompassWindArrow.Style2))
            compass.setValue(60.0)
        elif pos == 2:
            colorGroup.setColor(QColorGroup.Base, Qt.darkBlue)
            colorGroup.setColor(QColorGroup.Foreground,
                                QColor(Qt.darkBlue).dark(120))
            colorGroup.setColor(QColorGroup.Text, Qt.white)
            compass.setScaleTicks(1, 1, 3)
            compass.setScale(36, 5, 0)
            compass.setNeedle(
                QwtCompassMagnetNeedle(QwtCompassMagnetNeedle.ThinStyle))
            compass.setValue(220.0)
        elif pos == 3:
            colorGroup.setColor(QColorGroup.Base,
                                self.paletteBackgroundColor())
            colorGroup.setColor(QColorGroup.Foreground, Qt.blue)
            compass.setLineWidth(0)
            compass.scaleDraw().setOptions(compass.scaleDraw().options()
                                           | QwtScaleDraw.Backbone)
            compass.setScaleOptions(QwtDial.ScaleBackbone
                                    | QwtDial.ScaleTicks
                                    | QwtDial.ScaleLabel)
            compass.setScaleTicks(0, 0, 3)
            compass.setLabelMap({  0.0:   '0',
                                  60.0:  '60',
                                 120.0: '120',
                                 180.0: '180',
                                 240.0: '240',
                                 320.0: '320'})
            compass.setScale(36, 5, 0)
            compass.setNeedle(
                QwtDialSimpleNeedle(QwtDialSimpleNeedle.Ray, False, Qt.white))
            compass.setOrigin(220.0)
            compass.setValue(20.0)
        elif pos == 4:
            compass.setScaleTicks(0, 0, 3)
            compass.setNeedle(QwtCompassMagnetNeedle(
                QwtCompassMagnetNeedle.TriangleStyle, Qt.white, Qt.red))
            compass.setValue(220.0)
        elif pos == 5:
            colorGroup.setColor(QColorGroup.Foreground, Qt.black)
            compass.setNeedle(
                QwtDialSimpleNeedle(QwtDialSimpleNeedle.Ray, False, Qt.yellow))
            compass.setValue(315.0)

        palette = compass.palette()
        for cr in enumColorRoles():
            if colorGroup.color(cr).isValid():
                for cg in enumColorGroups():
                    palette.setColor(cg, cr, colorGroup.color(cr))

        for cg in enumColorGroups():
            light = palette.color(cg, QColorGroup.Base).light(170)
            dark = palette.color(cg, QColorGroup.Base).dark(170)
            if compass.frameShadow() == QwtDial.Raised:
                mid = palette.color(cg, QColorGroup.Base).dark(110)
            else:
                mid = palette.color(cg, QColorGroup.Base).light(110)

            palette.setColor(cg, QColorGroup.Dark, dark)
            palette.setColor(cg, QColorGroup.Mid, mid)
            palette.setColor(cg, QColorGroup.Light, light)

        compass.setPalette(palette)

    # __createCompass()

# class CompassGrid


class SpeedoMeter(QwtDial):

    def __init__(self, *args):
        QwtDial.__init__(self, *args)
        self.__label = 'km/h'
        self.setWrapping(False)
        self.setReadOnly(True)

        self.setOrigin(135.0)
        self.setScaleArc(0.0, 270.0)

        self.setNeedle(QwtDialSimpleNeedle(
            QwtDialSimpleNeedle.Arrow, True, Qt.red, Qt.gray.light(130)))

        self.setScaleOptions(QwtDial.ScaleTicks | QwtDial.ScaleLabel)
        self.setScaleTicks(0, 4, 8)

    # __init__()
    
    def setLabel(self, text):
        self.__label = text

    # setLabel()
    
    def label(self):
        return self.__label

    # label()
    
    def drawScaleContents(self, painter, center, radius):
        rect = QRect(0, 0, 2 * radius, 2 * radius - 10)
        rect.moveCenter(center)
        painter.setPen(self.colorGroup().text())
        painter.drawText(rect, Qt.AlignBottom | Qt.AlignHCenter, self.__label)

    # drawScaleContents

# class SpeedoMeter


class AttitudeIndicatorNeedle(QwtDialNeedle):

    def __init__(self, color):
        QwtDialNeedle.__init__(self)
        palette = QPalette()
        for cg in enumColorGroups():
            palette.setColor(cg, QColorGroup.Text, color)
        self.setPalette(palette)

    # __init__()
    
    def draw(self, painter, center, length, direction, cg):
        direction *= math.pi / 180.0
        triangleSize = int(round(length * 0.1))

        painter.save()

        p0 = QPoint(center.x() + 1, center.y() + 1)
        p1 = qwtPolar2Pos(p0, length - 2 * triangleSize - 2, direction)

        pa = QPointArray(3)
        pa.setPoint(0, qwtPolar2Pos(p1, 2 * triangleSize, direction))
        pa.setPoint(1, qwtPolar2Pos(p1, triangleSize, direction + math.pi/2))
        pa.setPoint(2, qwtPolar2Pos(p1, triangleSize, direction - math.pi/2))

        painter.setBrush(self.colorGroup(cg).text())
        painter.drawPolygon(pa)

        painter.setPen(QPen(self.colorGroup(cg).text(), 3))
        painter.drawLine(qwtPolar2Pos(p0, length - 2, direction + math.pi/2),
                         qwtPolar2Pos(p0, length - 2, direction - math.pi/2))

        painter.restore()

    # draw()

# class AttitudeIndicatorNeedle


class AttitudeIndicator(QwtDial):

    def __init__(self, *args):
        QwtDial.__init__(self, *args)
        self.__gradient = 0.0
        self.setMode(QwtDial.RotateScale)
        self.setWrapping(True)
        self.setOrigin(270.0)
        self.setScaleOptions(QwtDial.ScaleTicks)
        self.setScale(0, 0, 30.0)
        self.setNeedle(AttitudeIndicatorNeedle(self.colorGroup().text()))

    # __init__()

    def angle(self):
        return self.value()

    # angle()
    
    def setAngle(self, angle):
        self.setValue(angle)

    # setAngle()

    def gradient(self):
        return self.__gradient

    # gradient()

    def setGradient(self, gradient):
        self.__gradient = gradient

    # setGradient()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.setGradient(self.gradient() + 0.05)
        elif event.key() == Qt.Key_Minus:
            self.setGradient(self.gradient() - 0.05)
        else:
            QwtDial.keyPressEvent(self, event)

    # keyPressEvent()

    def drawScale(self, painter, center, radius, origin, minArc, maxArc):
        dir = (360.0 - origin) * math.pi / 180.0
        offset = 4
        p0 = qwtPolar2Pos(center, offset, dir + math.pi)

        w = self.contentsRect().width()

        # clip region to swallow 180 - 360 degrees
        pa = QPointArray(4)
        pa.setPoint(0, qwtPolar2Pos(p0, w, dir - math.pi/2))
        pa.setPoint(1, qwtPolar2Pos(
            QPoint(*pa.point(0)), 2 * w, dir + math.pi/2))
        pa.setPoint(2, qwtPolar2Pos(
            QPoint(*pa.point(1)), w, dir))
        pa.setPoint(3, qwtPolar2Pos(
            QPoint(*pa.point(2)), 2 * w, dir - math.pi/2))

        painter.save()
        painter.setClipRegion(QRegion(pa))
        QwtDial.drawScale(
            self, painter, center, radius, origin, minArc, maxArc)
        painter.restore()

    # drawScale()
    
    def drawScaleContents(self, painter, center, radius):
        dir = 360 - int(round(self.origin() - self.value()))
        arc = 90 + int(round(self.gradient() * 90))
        skyColor = QColor(38, 151, 221)
        painter.save()
        painter.setBrush(skyColor)
        painter.drawChord(
            self.scaleContentsRect(), (dir - arc)*16, 2*arc*16)
        painter.restore()

    # drawScaleContents()

# class AttitudeIndicator


class CockpitGrid(QGrid):
    
    def __init__(self, *args):
        QGrid.__init__(self, 3, *args)
        self.setPalette(self.__colorTheme(Qt.darkGray.dark(150)))
        for pos in range(3):
            self.__createDial(pos)
        layout = self.layout()
        for col in range(layout.numCols()):
            layout.setColStretch(col, 1)
        self.__speed_offset = 0.8
        self.__angle_offset = 0.05
        self.__gradient_offset = 0.005
            
    # __init__()
    
    def __colorTheme(self, base):
        background = base.dark(150)
        foreground = base.dark(200)
        
        mid = base.dark(110)
        dark = base.dark(170)
        light = base.light(170)
        text = foreground.light(800)

        cg = QColorGroup()
        cg.setColor(QColorGroup.Base, base)
        cg.setColor(QColorGroup.Background, background)
        cg.setColor(QColorGroup.Mid, mid)
        cg.setColor(QColorGroup.Light, light)
        cg.setColor(QColorGroup.Dark, dark)
        cg.setColor(QColorGroup.Text, text)
        cg.setColor(QColorGroup.Foreground, foreground)
        
        palette = QPalette()
        palette.setActive(cg)
        palette.setDisabled(cg)
        palette.setInactive(cg)

        return palette

    # __colorTheme()

    def __createDial(self, pos):
        dial = None
        if pos == 0:
            self.__clock = QwtAnalogClock(self)
            knobColor = Qt.gray.light(130)
            for h in enumHands():
                handColor = Qt.gray.light(150)
                width = 8
                if h == QwtAnalogClock.SecondHand:
                    handColor = Qt.gray
                    width = 5

                hand = QwtDialSimpleNeedle(
                    QwtDialSimpleNeedle.Arrow, True, handColor, knobColor)
                hand.setWidth(width)
                self.__clock.setHand(h, hand)
            timer = QTimer(self.__clock)
            timer.connect(timer, SIGNAL('timeout()'),
                          self.__clock, SLOT('setCurrentTime()'))
            timer.start(1000)
            dial = self.__clock
        elif pos == 1:
            self.__speedo = SpeedoMeter(self)
            self.__speedo.setRange(0.0, 240.0)
            self.__speedo.setScale(-1, 2, 20)
            timer = QTimer(self.__speedo)
            timer.connect(timer, SIGNAL('timeout()'), self.changeSpeed)
            timer.start(50)
            dial = self.__speedo
        elif pos == 2:
            self.__ai = AttitudeIndicator(self)
            gradientTimer = QTimer(self.__ai)
            gradientTimer.connect(
                gradientTimer, SIGNAL('timeout()'), self.changeGradient)
            gradientTimer.start(100)
            angleTimer = QTimer(self.__ai)
            angleTimer.connect(
                angleTimer, SIGNAL('timeout()'), self.changeAngle)
            angleTimer.start(100)
            dial = self.__ai

        if dial:
            dial.setReadOnly(True)
            dial.scaleDraw().setPenWidth(3)
            dial.setLineWidth(4)
            dial.setFrameShadow(QwtDial.Sunken)

    # __createDial()

    def changeSpeed(self):
        speed = self.__speedo.value()
        if ((speed < 40.0 and self.__speed_offset < 0.0)
            or (speed > 200.0 and self.__speed_offset > 0.0)):
            self.__speed_offset = -self.__speed_offset
        r = random.randrange(12)
        if r < 6:
            self.__speedo.setValue(speed + r*self.__speed_offset)

    # changeSpeed()

    def changeAngle(self):
        angle = self.__ai.angle()
        if angle > 180.0:
            angle -= 360.0

        if ((angle < -7.0 and self.__angle_offset < 0.0 )
            or (angle > 7.0 and self.__angle_offset > 0.0)):
            self.__angle_offset = -self.__angle_offset
            
        self.__ai.setAngle(angle + self.__angle_offset)

    # changeAngle()

    def changeGradient(self):
        gradient = self.__ai.gradient()

        if ((gradient < -0.05 and self.__gradient_offset < 0.0 )
            or (gradient > 0.05 and self.__gradient_offset > 0.0)):
            self.__gradient_offset = -self.__gradient_offset

        self.__ai.setGradient(gradient + self.__gradient_offset)

    # changeGradient()

# class CockpitGrid


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()

# main()

def make():
    demo = QTabWidget()
    demo.addTab(CompassGrid(demo), "Compass")
    demo.addTab(CockpitGrid(demo), "Cockpit")
    demo.show()
    return demo

# make()

# Admire!
if __name__ == '__main__':
    main(sys.argv)
    
# Local Variables: ***
# mode: python ***
# End: ***
