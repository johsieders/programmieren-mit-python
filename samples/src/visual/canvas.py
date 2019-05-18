## js 4.8.04
## tkinter revisited

from Tkinter import *


class App(object):
    def __init__(self, master):
        self.i = 0
        frame = Frame(master)
        frame.pack()

        self.canvas = Canvas(frame, height=500, width=500, bg='lightyellow')
        self.canvas.pack()

        self.xy = 20, 20, 480, 480
        self.arcs = [None] * 3

        self.button = Button(frame, text='Quit', command=frame.quit)
        self.button.pack(side=LEFT)

        self.delete = Button(frame, text='<', command=self.delete)
        self.delete.pack(side=LEFT)

        self.build = Button(frame, text='>', command=self.build)
        self.build.pack(side=LEFT)

    def delete(self):
        self.canvas.delete(self.arcs[self.i])
        self.i -= 1
        self.i %= 3

    def build(self):
        if self.i == 0:
            self.arcs[self.i] = self.canvas.create_arc(self.xy, start=0, extent=270, fill='red')
            self.i += 1
        elif self.i == 1:
            self.arcs[self.i] = self.canvas.create_arc(self.xy, start=270, extent=60, fill='blue')
            self.i += 1
        elif self.i == 2:
            self.arcs[self.i] = self.canvas.create_arc(self.xy, start=330, extent=30, fill='green')


root = Tk()
app = App(root)

root.mainloop()
