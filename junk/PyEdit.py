#!/usr/bin/env python

import sys
from PQTokenize import *
from keyword import *

from qt import *

class PyEdit(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)

        # user interface setup
        self.setTextFormat(QTextEdit.PlainText)
        #self.setWrapPolicy(QTextEdit.Anywhere)
        self.setCaption('PyEdit -- a Python Editor for PyQt')
        font = QFont("Fixed", 12)
        font.setFixedPitch(1)
        self.setFont(font)

        # geometry
        height = 40*QFontMetrics(font).lineSpacing()
        request = QSize(600, height)
        if parent is not None:
            request = request.boundedTo(parent.size())
        self.resize(request)

        self.y = 0
        self.x = 0

    def __insertWhite(self, y, x):
        if (y > self.y): # whitespace after a newline
            self.insertAt(' '*x, y, 0)
        else: # whitespace between tokens on the same line
            self.insertAt(' '*(x-self.x), y, self.x)

    def __insertToken(self, token, sy, sx, ey, ex):
        self.insertAt(token, sy, sx)
        self.y, self.x = ey, ex

    def fontify(self, type, token, (sy, sx), (ey, ex), line):
        """
        Insert fontified text at the current cursor position.
        """
        print "(%d,%d)->(%d,%d):\t%s\t%s" % \
              (sy, sx, ey, ex, tok_name[type], repr(token))
        
        self.__insertWhite(sy, sx)
        
        if type == NAME:
            if iskeyword(token):
                self.setBold(1)    
        elif type == STRING:
            self.setColor(Qt.darkGreen)
        elif type == 52:
            self.setColor(Qt.red)

        self.__insertToken(token, sy, sx, ey, ex)
        
        self.setBold(0)
        if type == 1 and token in ['class', 'def']:
            self.setColor(Qt.blue)
        else:
            self.setColor(Qt.black)
        
    def focusNextPrevChild(self, next):
        """
        Suppress tabbing to the next window in multi-line commands. 
        """
        if next and self.more:
            return 0
        return QTextEdit.focusNextPrevChild(self, next)

    def mousePressEvent(self, e):
        """
        Keep the cursor after the last prompt.
        """
        if e.button() == Qt.LeftButton:
            self.moveCursor(QTextEdit.MoveEnd, 0)
        return

    def contentsContextMenuEvent(self,ev):
        """
        Suppress the right button context menu.
        """
        return

        
if __name__ == '__main__':

    a = QApplication(sys.argv)
    w = PyEdit()
    a.setMainWidget(w)

    file = open('PyEdit.py')
    tokenize(file.readline, w.fontify)

    file.close()
    
    w.show()
    
    a.exec_loop()
