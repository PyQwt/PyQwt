# Set your PYTHONSTARTUP environment variable to $HOME/.pythonrc.py
#
# inspired by:
# http://opag.ca/wiki/OpagSnippets?action=highlight&value=pythonrc

from atexit import register
from os import path
import readline
import rlcompleter
# to use PyQt widgets from the command line interpreter
import iqt

# I use a tab for completion and a single space to indent Python code
readline.parse_and_bind('tab: complete')

historyPath = path.expanduser('~/.python_history')
readline.set_history_length(1000)

def save_history(historyPath=historyPath):
    import readline
    # why fails the next line to see the global readline?
    readline.write_history_file(historyPath)

if path.exists(historyPath):
    readline.read_history_file(historyPath)

register(save_history)

del register, path, readline, rlcompleter, iqt, historyPath, save_history

# to use scipy, qwt and qt
from scipy import *
from qwt import *
from qt import *

# to use tab completion with for instance 'help(scipy.optimize.leastsq)'
import scipy

# Local Variables: ***
# mode: python ***
# End: ***
