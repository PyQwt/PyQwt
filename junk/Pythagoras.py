#!/usr/bin/env python

import os, sys
from qt import *
from PyCute import PyCute

class Pythagoras(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,)+args)

        self.fileMenu = QPopupMenu()
        self.actionExit = QAction(
            "Exit", "E&xit", QAccel.stringToKey("CTRL+X"), self)
        self.actionExit.addTo(self.fileMenu)
        self.connect(
            self.actionExit, SIGNAL("activated()"), self.onExit)
        self.menuBar().insertItem("&File", self.fileMenu)

        self.menuBar().insertSeparator()

        self.helpMenu = QPopupMenu()
        self.actionPyLibDoc = QAction(
            "PyLibDoc", "PyLibDoc", QAccel.stringToKey(""), self)
        self.connect(
            self.actionPyLibDoc, SIGNAL("activated()"), self.onPyLibDoc)
        self.actionPyLibDoc.addTo(self.helpMenu)
        self.actionPyDocDoc = QAction(
            "PyDocDoc", "PyDocDoc", QAccel.stringToKey(""), self)
        self.actionPyDocDoc.addTo(self.helpMenu)
        self.menuBar().insertItem("&Help", self.helpMenu)
        
        self.resize(640, 640)
        self.shell = PyCute(None, None, None, parent=self)
        self.setCentralWidget(self.shell)

        self.shell.fakeUser([
            'from Numeric import *',
            'from plot import *',
            'dir()',
            ])

    def onExit(self):
        qApp.quit()

    def onPyLibDoc(self):
        # dillo is a fast lightweight Gtk web browser, recommended!
        cmd = ['dillo', '/usr/share/doc/Python-2.2.1/index.html']
        os.spawnvpe(os.P_NOWAIT, 'dillo', cmd, os.environ)
 
    def onPyDocDoc(self):
        pass

# Admire
___a___ = QApplication(sys.argv)
___w___ = Pythagoras()
___a___.setMainWidget(___w___)
___w___.show()
___a___.exec_loop()
