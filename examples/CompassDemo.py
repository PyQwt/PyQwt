#!/usr/bin/env python

import sys
from qt import *
from qwt import *

class Compass1(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setMode(QwtCompass.RotateScale)
        self.setLineWidth(6)
        self.setFrameShadow(QFrame.Sunken)
        rose = QwtSimpleCompassRose(16, 2)
        rose.setWidth(0.15)
        self.setRose(rose)

    # __init__()

# class Compass1

class Compass2(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setLineWidth(6)        
        self.setFrameShadow(QFrame.Sunken)
        self.setLabelMap({0.0: 'n',
                          90.0: 'o',
                          180.0: 'z',
                          270.0: 'w',
                          })
        for k, v in self.labelMap().items():
            print k, v
        self.setRose(QwtSimpleCompassRose(4, 1))
        self.setNeedle(QwtCompassWindArrow(QwtCompassWindArrow.Style2))
        self.setValue(60.0)

    # __init__()

# class Compass2
 
class Compass3(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setLineWidth(6)        
        self.setFrameShadow(QFrame.Raised)
        self.scaleDraw().setTickLength(0, 0, 3)
        self.setNeedle(QwtCompassMagnetNeedle(
            QwtCompassMagnetNeedle.TriangleStyle, Qt.blue, Qt.red))
        self.setValue(220.0)

    # __init__()

# class Compass3
 
class Compass4(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setLineWidth(6)
        self.setFrameShadow(QFrame.Raised)
        p = self.palette()
        for i in range(QPalette.NColorGroups):
            p.setColor(i, QColorGroup.Foreground, Qt.black)
        self.setPalette(p)
        self.setNeedle(QwtDialSimpleNeedle(
            QwtDialSimpleNeedle.Ray, 0, Qt.yellow))
        self.setValue(315.0)

    # __init__()

# class Compass4

class Compass5(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.setLineWidth(6)
        self.setFrameShadow(QFrame.Sunken)

        self.scaleDraw().setTickLength(1, 1, 3)
        self.setScale(36, 5, 0);

        self.setNeedle(QwtCompassMagnetNeedle(
            QwtCompassMagnetNeedle.ThinStyle))
        self.setValue(220.0)

        p = self.palette()
        for i in range(QPalette.NColorGroups):
            p.setColor(i, QColorGroup.Base, p.color(i, QColorGroup.Background))
            p.setColor(i, QColorGroup.Foreground, Qt.darkBlue)
            p.setColor(i, QColorGroup.Text, Qt.white)
        self.setPalette(p)

    # __init__()

# class Compass5

class Compass6(QwtCompass):
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        p = self.palette()
        for i in range(QPalette.NColorGroups):
            p.setColor(i, QColorGroup.Base, p.color(i, QColorGroup.Background))
            p.setColor(i, QColorGroup.Foreground, Qt.blue)
        self.setPalette(p)

        self.scaleDraw().setOptions(
            self.scaleDraw().options() | QwtScaleDraw.Backbone)
        self.scaleDraw().setTickLength(0, 0, 3);

        map = {}
        for i in range(0, 360, 60):
            map[float(i)] = "%.0f" % float(i)
        self.setLabelMap(map)
        self.setScale(36, 5, 0);
        
        self.setNeedle(QwtDialSimpleNeedle(
            QwtDialSimpleNeedle.Ray, 1, Qt.white, Qt.gray))
        self.setOrigin(220.0)
        self.setValue(20.0)

    # __init__()

# class Compass6


def main(args):
    app = QApplication(args)
    demo = make()
    app.setMainWidget(demo)
    app.exec_loop()


def make():
    demo = QGrid(3)
    Compass1(demo)
    Compass2(demo)
    Compass3(demo)
    Compass4(demo)
    Compass5(demo)
    Compass6(demo)
    demo.resize(600, 400)
    demo.show()
    return demo


# Admire!
if __name__ == '__main__':
    main(sys.argv)
    


