#!/usr/bin/env python

from Tkinter import *

def doit():
    any_error

frame = Frame()
frame.pack()
crashme = Button(frame, text="Crash Me", command=doit)
crashme.pack()
frame.mainloop()
