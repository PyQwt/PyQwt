#!/usr/bin/env python

from qt import *
import iqt

def doit():
    raise SystemExit, "Hang Me"

hangme = QPushButton("Hang Me", None)
hangme.connect(hangme, SIGNAL("clicked()"), doit)
hangme.show()
