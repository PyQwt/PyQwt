#!/usr/bin/python

# In the future PyCute will get more features of the Idle's Python shell:
# - fontification (syntax coloring)
# - balloon help with documentation strings
# - copy & paste into or out of the shell
#
#
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

    """
    PyCute is a Python shell for PyQt.

    Creating, displaying and controlling PyQt widgets from the Python command
    line interpreter is very hard, if not, impossible.  PyCute solves this
    problem by interfacing the Python interpreter to a PyQt widget.

    My use is interpreter driven plotting to QwtPlot instances. Why?
    
    Other popular scientific software packages like SciPy, SciLab, Octave,
    Maple, Mathematica, GnuPlot, ..., also have interpreter driven plotting.  
    It is well adapted to quick & dirty exploration. 

    Of course, PyQt's debugger -- eric -- gives you similar facilities, but
    PyCute is smaller and easier to integrate in applications.
    Eric requires Qt-3.x

    PyCute is based on ideas and code from:
    - Python*/Tools/idle/PyShell.py (Python Software Foundation License)
    - PyQt*/eric/Shell.py (Gnu Public License)
    """
    
    def __init__(self, locals=None, log='', parent=None):
        """Constructor.

        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.

        The optional 'log' argument specifies the file in which the
        interpreter session is to be logged.
        
        The optional 'parent' argument specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """

        QTextEdit.__init__(self, parent)
        self.interpreter = Interpreter(locals)

        # session log
        self.log = log or ''

        # to exit the main interpreter by a Ctrl-D if PyCute has no parent
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None

        # capture all interactive input/output 
        sys.stdout   = self
        sys.stderr   = self
        sys.stdin    = self
        # last line + last incomplete lines
        self.line    = QString()
        self.lines   = []
        # the cursor position in the last line
        self.point   = 0
        # flag: the interpreter needs more input to run the last lines. 
        self.more    = 0
        # flag: readline() is being used for e.g. raw_input() and input()
        self.reading = 0
        # history
        self.history = []
        self.pointer = 0
        self.xLast   = 0
        self.yLast   = 0

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
                   ' for more information on Python.\n')
        self.write(sys.ps1)

    def flush(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        pass

    def isatty(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        return 1

    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QTextEdit.MoveEnd, 0)
        while self.reading:
            qApp.processOneEvent()
        if self.line.length() == 0:
            return '\n'
        else:
            return str(self.line) 
    
    def write(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        # The output of self.append(text) contains to many newline characters,
        # so work around QTextEdit's policy for handling newline characters.
        hack = self.text()
        hack.append(text)
        self.setText(hack)
        #self.setText(self.text().append(text)) # segmentation fault
        self.moveCursor(QTextEdit.MoveEnd, 0)
        self.yLast, self.xLast = self.getCursorPosition()

    def writelines(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        map(self.write, text)
        print "DO WE EVER GET HERE? IF YES, OPTIMIZATION POSSIBLE"

    def fakeUser(self, lines):
        """
        Simulate a user: lines is a sequence of strings, (Python statements).
        """
        for line in lines:
            self.line = QString(line.rstrip())
            self.write(self.line)
            self.write('\n')
            self.__run()
            
    def __run(self):
        """
        Append the last line to the history list, let the interpreter execute
        the last line(s), and clean up accounting for the interpreter results:
        (1) the interpreter succeeds
        (2) the interpreter fails, finds no errors and wants more line(s)
        (3) the interpreter fails, finds errors and writes them to sys.stderr
        """
        self.pointer = 0
        self.history.append(QString(self.line))
        self.lines.append(str(self.line))
        source = '\n'.join(self.lines)
        self.more = self.interpreter.runsource(source)
        if self.more:
            self.write(sys.ps2)
        else:
            self.write(sys.ps1)
            self.lines = []
        self.__clearLine()
        
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line.truncate(0)
        self.point = 0
        
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """
        y, x = self.getCursorPosition()
        self.insertAt(text, y, x)
        self.line.insert(self.point, text)
        self.point += text.length()
        self.setCursorPosition(y, x + text.length())

    def keyPressEvent(self, e):
        """
        Handle user input a key at a time.
        """
        text  = e.text()
        key   = e.key()
        ascii = e.ascii()

        if text.length() and ascii>=32 and ascii<127:
            self.__insertText(text)
            return

        if e.state() & Qt.ControlButton and key == self.eofKey:
            try:
                file = open(self.log, "w")
                file.write(str(self.text()))
                file.close()
            except:
                pass
            sys.exit()
            return
        
        if e.state() & Qt.ControlButton or e.state() & Qt.ShiftButton:
            e.ignore()
            return

        if key == Qt.Key_Backspace:
            if self.point:
                self.doKeyboardAction(QTextEdit.ActionBackspace)
                self.point -= 1
                self.line.remove(self.point, 1)
        elif key == Qt.Key_Delete:
            self.doKeyboardAction(QTextEdit.ActionDelete)
            self.line.remove(self.point, 1)
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.write('\n')
            if self.reading:
                self.reading = 0
            else:
                self.__run()
        elif key == Qt.Key_Tab:
            self.__insertText(text)
        elif key == Qt.Key_Left:
            if self.point:
                self.moveCursor(QTextEdit.MoveBackward, 0)
                self.point -= 1
        elif key == Qt.Key_Right:
            if self.point < self.line.length():
                self.moveCursor(QTextEdit.MoveForward, 0)
                self.point += 1
        elif key == Qt.Key_Home:
            self.setCursorPosition(self.yLast, self.xLast)
            self.point = 0
        elif key == Qt.Key_End:
            self.moveCursor(QTextEdit.MoveLineEnd, 0)
            self.point = self.line.length()
        elif key == Qt.Key_Up:
            if len(self.history):
                if self.pointer == 0:
                    self.pointer = len(self.history)
                self.pointer -= 1
                self.__recall()
        elif key == Qt.Key_Down:
            if len(self.history):
                self.pointer += 1
                if self.pointer == len(self.history):
                    self.pointer = 0
                self.__recall()
        else:
            e.ignore()

    def __recall(self):
        """
        Display the current item from the command history.
        """
        self.setCursorPosition(self.yLast, self.xLast)
        self.setSelection(self.yLast, self.xLast,
                          self.yLast, self.paragraphLength(self.yLast))
        self.removeSelectedText()
        self.__clearLine()
        self.__insertText(self.history[self.pointer])

        
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

# Local Variables: ***
# mode: python ***
# End: ***
