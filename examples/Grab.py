#!/usr/bin/env python
#
# Usage on Posix:
#       python [-i] Grab.py
# or:
#       python PyCute.py Grab.py
#
# Usage on Windows:
#       python PyCute.py Grab.py

# a list of .py files defining a function make()
# make() must initialize, show and return:
#       a QWidget
# or:
#       a tuple of QWidgets
jobs = [
    'BodeDemo',
    'CPUplot',
    'CliDemo1',
    'CliDemo2',
    'CurveDemo1',
    'CurveDemo2',
    'CurveDemo3',
    'DataDemo',
    'DialDemo',
    'ErrorBarDemo',
    'EventFilterDemo',
    'MapDemo',
    'MultiDemo',
    'PyCute',
    'QwtImagePlotDemo',
    'RadioDemo',
    'SimpleDemo',
    'SliderDemo',
    'StackOrder',
    ]

def expose(jobs, cache = {}):
    for job in jobs:
        result = __import__(job).make()
        if type(result) == type(()):
            for i in range(len(result)):
                cache['%s%s' % (job, i)] = result[i]
        else:
            cache[job] = result
    return cache

def save(cache):
    for name, widget in cache.items():
        pixmap = QPixmap.grabWidget(widget)
        pixmap.save(name+'.png', 'PNG')

def closeEventLoop():
    try:
        qApp.argc()
    except RuntimeError:
        try:
            import iqt
        except ImportError:
            print "Failed to import 'iqt', try 'python PyCute.py Grab.py'"
            raise


if __name__ == '__main__':
    from qt import *
    closeEventLoop()

    cache = expose(jobs)
    raw_input("Are all widgets looking HAPPY? ")
    save(cache)
