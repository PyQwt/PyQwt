#!/usr/bin/env python

import os
import popen2
import time

class GracePlotter:
    def __init__ (self, debug = None):
        self.debug = debug
        self.p = popen2.Popen3 ("xmgrace -nosafe -noask -dpipe 0")
        self.command("view xmin 0.15")
        self.command("view xmax 0.85")
        self.command("view ymin 0.15")
        self.command("view ymax 0.85")
        self.flush()
        self.curves = 0

    def command(self, cmd):
        if self.debug:
            print cmd
        self.p.tochild.write(cmd + '\n')

    def flush(self):
        #self.command('redraw')
        self.p.tochild.flush()

    def wait(self):
        return self.p.wait()

    def kill(self):
        os.kill(self.p.pid, 9)

    def __call__(self, cmd):
        self.command(cmd)


if __name__ == '__main__':
    g = GracePlotter()
    g('world xmax 100')
    g('world ymax 10000')
    g('xaxis tick major 20')
    g('xaxis tick minor 10')
    g('yaxis tick major 2000')
    g('yaxis tick minor 1000')
    g('s0 on')
    g('s0 symbol 1')
    g('s0 symbol size 0.3')
    g('s0 symbol fill pattern 1')
    g('s1 on')
    g('s1 symbol 1')
    g('s1 symbol size 0.3')
    g('s1 symbol fill pattern 1')

    # Display sample data
    for i in range(1,101):
        g('g0.s0 point %d, %d' % (i, i))
        g('g0.s1 point %d, %d' % (i, i * i))
        # Update the Grace display after every ten steps
        if i % 10 == 0:
            g('redraw')
            g.flush()
            # Wait a second, just to simulate some time needed for
            # calculations. Your real application shouldn't wait.
            time.sleep(1)

    # Tell Grace to save the data:
    g('saveall "sample.agr"')

    # Close Grace:
    g.wait()
