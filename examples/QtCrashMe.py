#!/usr/bin/env python

from qt import *
import iqt

def doit():
    any_error

crashme = QPushButton("Crash Me", None)
crashme.connect(crashme, SIGNAL("clicked()"), doit)
crashme.show()
