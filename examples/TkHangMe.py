#!/usr/bin/env python

from Tkinter import *

def doit():
    raise SystemExit, "Hang Me"

frame = Frame()
frame.pack()
hangme = Button(frame, text="Hang Me", command=doit)
hangme.pack()
frame.mainloop()

