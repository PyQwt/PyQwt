#!/usr/bin/env python

from PQTokenize import *
from keyword import *
from cStringIO import StringIO

class Tagger:

    def __init__(self, file):
        self.file = file

    def tokeneater(self, type, token, (srow, scol), (erow, ecol), line):
        if self.row != srow:
            self.row = srow
            if self.line:
                self.tags.append(self.line)
            if scol:
                self.line = [(0, "black", "normal", repr(token))]
            else:
                self.line = []
        if type == NAME:
            if iskeyword(token):
                self.line.append((scol, "black", "bold", repr(token)))
        elif type == STRING:
            self.line.append((scol, "green", "normal", repr(token)))
        elif type == COMMENT:
            self.line.append((scol, "red", "normal", repr(token)))
        else:
            self.line.append((scol, "black", "normal", repr(token)))
        #print "(%d,%d)->(%d,%d):\t%s\t%s" % \
        #      (srow, scol, erow, ecol, tok_name[type], repr(token))
              
    def __call__(self):
        self.tags = []
        #self.text = []
        self.line = []
        self.col = 0
        self.row = -1
        tokenize(self.file.readline, self.tokeneater)
        return self.tags

if __name__ == '__main__':

    file = open("xtokenize.py")
    text = StringIO(file.read())
    file.close
    tagger = Tagger(text)
    tags = tagger()
    for tag in tags:
        print tag

    
