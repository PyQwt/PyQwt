#!/usr/bin/env python

# Did you find a bug in PyCute? Check Idle's behavior before reporting.
#
# There will be always some differences between a GUI shell and the Python
# interpreter running in a terminal (Unix) or DOS box (Windows), e.g:
#
# os.system('dir') or os.system('ls')
#
# In a terminal or DOS box, the user sees the directory listing followed by
# the return code (0). Why? In this case, stdout of the 'dir' or 'ls' command
# coincides with stdout of the interpreter.
#
# This is not the case with a GUI shell like PyCute or Idle. If the shell has
# been started from a terminal or DOS box, the directory listing will appear
# in the terminal or DOS box and the return code will appear in the GUI shell.
# If the GUI shell has been started by other means, the return code of the
# command will appear in the shell but the other behavior of is undefined
# (under Unix you will see nothing, and under Windows you will see
# a DOS box flashing up).

import os, sys
from code import InteractiveInterpreter as Interpreter
from qt import *

class PyCute(QTextEdit):

    reading = 0
    history = []
    pointer = 0

    def __init__(self, locals=None, log='', parent=None):
        """Constructor.

        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.

        The optional 'log' argument specifies the file in which the
        interpreter session is to be logged.

        The optional 'parent' argument specifies the parent widget.
        If no parent widget has been specified, you can exit the
        interpreter by typing Ctrl-D.
        """

        QTextEdit.__init__(self)
        self.interpreter = Interpreter(locals)
        self.connect(self, SIGNAL("returnPressed()"), self.onReturnPressed)

        # session log
        self.log = log or 'PyCute.log'

        # to exit the main interpreter by a Ctrl-D if PyCute has no parent
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None

        # capture all interactive input/output
        sys.stdout = self
        sys.stderr = self
        sys.stdin  = self

        # user interface setup
        self.setTextFormat(QTextEdit.PlainText)
        self.setWrapPolicy(QTextEdit.Anywhere)
        self.setCaption('PyCute -- a Python Shell for PyQt -- '
                        'http://gerard.vermeulen.free.fr')

        # font
        if os.name == 'posix':
            font = QFont("Fixed", 12)
        elif os.name == 'nt' or os.name == 'dos':
            font = QFont("Courier New", 8)
        else:
            raise SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'"
        font.setFixedPitch(1)
        self.setFont(font)

        # geometry
        height = 40*QFontMetrics(font).lineSpacing()
        request = QSize(600, height)
        if parent is not None:
            request = request.boundedTo(parent.size())
        self.resize(request)

        # interpreter prompt.
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "

        # interpreter banner
        self.write('The PyCute shell running Python %s on %s.\n' %
                   (sys.version, sys.platform))
        self.write('Type "copyright", "credits" or "license"'
                   ' for more information on Python.')
        self.ps1()

    # __init__()

    def write(self, line):
        self.append(line.rstrip('\n'))
        self.moveCursor(QTextEdit.MoveEnd, 0)

    # write()

    def flush(self):
        pass

    # flush()
    
    def ps1(self):
        self.append(sys.ps1)
        self.moveCursor(QTextEdit.MoveEnd, 0)
        self.mark = self.getCursorPosition()

    # ps1()

    def ps2(self):
        self.append(sys.ps2)
        self.moveCursor(QTextEdit.MoveEnd, 0)

    # ps2()

    def tab(self):
        self.insert('    ')
        self.moveCursor(QTextEdit.MoveEnd, 0)

    # tab()

    def getLines(self):
        apply(self.setSelection, self.mark + self.getCursorPosition())
        lines = self.selectedText()
        return str(lines)

    # getLines()
        
    def readline(self):
        lines = self.getLines()
        self.history.insert(0, (self.mark, lines))
        self.moveCursor(QTextEdit.MoveEnd, 0)
        self.mark = self.getCursorPosition()
        self.reading = 1
        while self.reading:
            qApp.processOneEvent()
        return self.getLines().rstrip() or '\n'

    # readline()
        
    def push(self):
        lines = self.getLines()
        if not self.interpreter.runsource(lines.replace(sys.ps2, '')):
            self.history.insert(0, (self.mark, lines))
            #print self.history
            self.ps1()
        else:
            self.ps2()

    # push()

    def onReturnPressed(self):
        if self.reading:
            self.reading = 0
        else:
            self.push()

    # onReturnPressed()

    def keyPressEvent(self, e):
        ascii = e.ascii()
        key   = e.key()
        state = e.state()
        text  = e.text()

        #print "'%s' '%s' '%s' '%s'" % (ascii, key, state, text)
        if state & Qt.ControlButton and key == self.eofKey:
            try:
                file = open(self.log, "w")
                file.write(str(self.text()))
                file.close()
            except:
                pass
            sys.exit()
            return

        if state & Qt.ControlButton and key == Qt.Key_I:
            self.tab()
            return

        if key == Qt.Key_Tab:
            # completion
            return
        
        if key == Qt.Key_Return and not self.reading:
            position = self.getCursorPosition()
            if self.mark > position:
                for mark, lines in self.history:
                    if mark < position:
                        apply(self.setCursorPosition, self.mark)
                        self.insert(lines.rstrip('\n'))
                        return
                else:
                    return

        QTextEdit.keyPressEvent(self, e)

    # keyPressEvent()

# class PyCute()
    
if __name__ == '__main__':
    __a__ = QApplication(sys.argv)
    __w__ = PyCute(locals=sys.modules['__main__'].__dict__)
    __a__.setMainWidget(__w__)
    __w__.show()
    __a__.exec_loop()

# Local Variables: ***
# mode: python ***
# End: ***
