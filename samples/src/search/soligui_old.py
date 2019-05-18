# GUI fuer Solitaer
# js 29.12.02

from Tkinter import *

from soli_old import *

# Buttons enthaelt alle Buttons als Matrix
Buttons = map(list, 7 * [7 * [None]])

# Liste der moeglichen Startpunkte
Starts = []

On = "gray"  # da steht ein Stein
Off = "white"  # da steht keiner
Start = "blue"  # alle Steine, die springen koennen
Selected = "yellow"  # der gewaehlte Start
End = "green"  # alle Endpunkte ausgehend von Start
Colours = (Off, On, Start, Selected, End)

cnt = 0  # Count-Label

# die gewaehlte Stelle, von der aus gesprungen wird
# es gilt: SelectedStart in Sources oder SelectedStart is None
SelectedStart = None

# Liste der moeglichen Endpunkte ausgehend von SelectedStart
Ends = []


# Das Spiel befindet sich immer in einem von zwei Zustaenden
# ZUSTAND A: Kein Startpunkt gewaehlt (SelectedStart is None)
#   Dann sind alle Punkte in Starts waehlbar (d.h.: der zugehoerige Button ist NORMAL)
#   Die Starts sind alle BLAU.
# ZUSTAND B: Genau ein Startpunkt gewaehlt (SelectedStart in Starts). Dann gilt:
#    1. Ends enthaelt genau die vom Startpunkt aus anspringbaren Punkte
#    2. Waehlbar sind der Startpunkt und alle Ends
#       Die Ends sind alle GRUEN, der gewaehlte Startpunkt ist GELB
#    3. Wahl des Startpunkts fuehrt zurueck in den Zustand A, 
#       d.h.: Der bisherige Startpunkt ist nicht mehr selektiert.
#    4. Wahl eines Endpunkts loest den Sprung zu diesem Endpunkt aus. Der Sprung wird durchgefuehrt;
#       das Spiel ist wieder im Zustand A. 

def adjustButtonsForA():
    """ kein Startpunkt selektiert, Ends == [] """
    assert not SelectedStart and not Ends  # Zustand A erwartet

    for x in range(7):
        for y in ypsilon(x):
            b = Buttons[x][y]
            if mayMove(x, y):
                b.config(state=NORMAL, bg=Start)
                Starts.append(b)
            else:
                b.config(state=DISABLED, bg=Colours[Board[x][y]])

    cnt.config(text="Anzahl = " + str(count()))


def adjustButtonsForB():
    """ Startpunkt selektiert, Ends != [] """
    assert SelectedStart and Ends  # Zustand B

    for b in Starts:
        b.config(state=DISABLED, bg=On)
    for b in Ends:
        b.config(state=NORMAL, bg=End)
    SelectedStart[2].config(state=NORMAL, bg=Selected)


def onClick(x, y):
    def tmp():
        global Starts, SelectedStart, Ends
        if not SelectedStart:  # im Zustand A
            SelectedStart = (x, y, Buttons[x][y])
            Ends = [Buttons[u][v] for (u, v) in getEnds(x, y)]
            adjustButtonsForB()  # Zustand B herbeifuehren
        else:  # im Zustand B
            move(SelectedStart[:2], (x, y))
            Starts = []
            SelectedStart = None
            Ends = []
            adjustButtonsForA()  # Zustand A herbeifuehren
        print
        x, y

    return tmp


def onReset():
    global Starts, SelectedStart, Ends
    resetBoard()
    Starts = []
    SelectedStart = None
    Ends = []
    adjustButtonsForA()


def makeView(root):
    global cnt, Buttons, Starts, SelectedStart, Ends
    board = Frame(root)

    for x in range(7):
        for y in ypsilon(x):
            b = Button(board, command=onClick(x, y))
            b.grid(row=x, column=y)
            Buttons[x][y] = b

    Starts = []
    SelectedStart = None
    Ends = []

    controls = Frame(root)
    rs = Button(controls, text="Reset", command=onReset)
    rs.grid(row=0, column=0)
    cnt = Label(controls, relief=RAISED)
    cnt.grid(row=0, column=1)

    board.pack(side=TOP)
    controls.pack(side=TOP)

    adjustButtonsForA()
    ### end makeView ###


if __name__ == "__main__":
    root = Tk()
    root.title("Solit�r")
    makeView(root)
    root.mainloop()
