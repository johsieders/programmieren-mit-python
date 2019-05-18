## some tests
## js 11.08.2004

from Tkinter import *
from tkColorChooser import *
from tkFileDialog import *

if __name__ == '__main__':
    c = askcolor()
    print
    c

    root = Tk()

    frame = Frame(root, height=1000, width=1000, bg=c[1])
    frame.pack()

    ##    canvas = Canvas(frame, height=1000, width=1000, bg=c[1])
    ##    canvas.pack()

    root.mainloop()

##    f = askopenfile()
##    print f
