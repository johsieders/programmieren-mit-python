# GUI fuer Solitaer
# js 29.12.02

from soli import *
from Tkinter import *

# Buttons enthaelt alle Buttons als Matrix
Buttons = {}

# ON ist die Belegung von BOARD
ON = initBoard()

# Liste der moeglichen Startpunkte
Starts = []

On       = "gray"           # da steht ein Stein
Off      = "white"          # da steht keiner
Start    = "blue"           # alle Steine, die springen koennen
Selected = "yellow"         # der gewaehlte Start
Target   = "green"          # alle Endpunkte ausgehend von Start
Colours = (Off, On, Start, Selected, Target)

cnt = 0 # Count-Label

# die gewaehlte Stelle, von der aus gesprungen wird
# es gilt: SelectedStart in Sources oder SelectedStart is None
SelectedStart = None

# Liste der moeglichen Endpunkte ausgehend von SelectedStart
Targets = []

# Das Spiel befindet sich immer in einem von zwei Zustaenden
# ZUSTAND A: Kein Startpunkt gewaehlt (SelectedStart is None)
#   Dann sind alle Punkte in Starts waehlbar (d.h.: der zugehoerige Button ist NORMAL)
#   Die Starts sind alle BLAU.
# ZUSTAND B: Genau ein Startpunkt gewaehlt (SelectedStart in Starts). Dann gilt:
#    1. Targets enthaelt genau die vom Startpunkt aus anspringbaren Punkte
#    2. Waehlbar sind der Startpunkt und alle Targets
#       Die Targets sind alle GRUEN, der gewaehlte Startpunkt ist GELB
#    3. Wahl des Startpunkts fuehrt zurueck in den Zustand A, 
#       d.h.: Der bisherige Startpunkt ist nicht mehr selektiert.
#    4. Wahl eines Endpunkts loest den Sprung zu diesem Endpunkt aus. Der Sprung wird durchgefuehrt;
#       das Spiel ist wieder im Zustand A. 

def adjustButtonsForA():
    """ kein Startpunkt selektiert, Targets == [] """
    assert not SelectedStart and not Targets  # Zustand A erwartet
    global ON
    
    for s in BOARD:
        b = Buttons[s]
        if mayMove(s, ON):
            b.config(state=NORMAL, bg=Start)
            Starts.append(b)
        else:
            b.config(state=DISABLED, bg=Colours[ON[s]])

    cnt.config(text="Anzahl = " + str(count(ON)))


def adjustButtonsForB():
    """ Startpunkt selektiert, Targets != [] """
    assert SelectedStart and Targets  # Zustand B
    
    for b in Starts:
        b.config(state=DISABLED, bg=On)
    for b in Targets:
        b.config(state=NORMAL, bg=Target)
    SelectedStart[1].config(state=NORMAL, bg=Selected)


def onClick(s):
    def tmp():
        global ON, Starts, SelectedStart, Targets
        if not SelectedStart:       # im Zustand A
            SelectedStart = (s, Buttons[s])
            Targets = [Buttons[t] for t in getTargets(s, ON)]
            adjustButtonsForB()     # Zustand B herbeifuehren
        else:                       # im Zustand B
            moveTo(SelectedStart[0], s, ON)
            Starts = []
            SelectedStart = None
            Targets = []
            adjustButtonsForA()    # Zustand A herbeifuehren
    return tmp


def onReset():
    global ON, Starts, SelectedStart, Targets
    ON = initBoard()
    Starts = []
    SelectedStart = None
    Targets = []
    adjustButtonsForA()


def makeView(root):
    global cnt, Buttons, ON, Starts, SelectedStart, Targets
    board = Frame(root)

    for s in BOARD:
        b = Button(board, command=onClick(s))
        b.grid(row=s[0], column=s[1])
        Buttons[s] = b

    Starts = []
    SelectedStart = None
    Targets = []

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
    root.title("Solitär")
    makeView(root)
    root.mainloop()