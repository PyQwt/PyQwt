#!/usr/bin/env python
# everything after a '#' is comment

import sys
from qt import *
from qwt import *

INIT_TESTS = 0 # always worked
INIT_TESTS = 2 # crashed on Qt<232, fixed

class ClearBugDemo(QwtPlot):
    def __init__(self, parent=None):
        QwtPlot.__init__(self, parent)
        for i in range(INIT_TESTS): # means: for(int i=0; i<INIT_TESTS; i++) {
            self.test()
        # end i-loop
    # end __init__()

    def test(self):
        self.removeCurves()
        print "entering enableLegend(0)"
        self.enableLegend(0)
        print "leaving enableLegend(0)"
        for j in range(3): # for(int j=0; j<3; j++) {
            key = self.insertCurve("test" + str(j))
            self.enableLegend(1, key)
        # end j-loop
    # end test()

# main()
if __name__ == '__main__':
    app = QApplication(sys.argv) # app = new QApplication(argv, argc);
    demo = ClearBugDemo()        # demo = new ClearBugDemo;
    app.setMainWidget(demo)      # app->setMainWidget(demo);
    demo.show()                  # app->show();
    for i in range(3):
        demo.test()              # app->show();
    app.exec_loop()              # means app->exec();

