## diverse Versuche zu den Queens
## js 10.8.02
## bubenorbis

from test.test_generators import conjoin

from search import SearchProblem


def nextPositions(n, state):
    """ liefert die Menge der sicheren Positionen in der naechsten Zeile.
    
        Beispiel: state = [3, 0] bedeutet:
        In Zeile 0 steht eine Koenigin auf Position 3
        in Zeile 1 steht eine Koenigin auf Position 0
        Sicher sind in Zeile 2 die Positionen 2, 4
        Ergebnis mit n = 5: [2, 4]
    """

    offlimits = set()
    k = len(state)
    for i in range(k):
        offlimits.add(state[i] - k + i)
        offlimits.add(state[i])
        offlimits.add(state[i] + k - i)

    return set(range(n)) - offlimits


class QueensProblem(SearchProblem):
    def __init__(self, size):
        self.__size = size  ## number of rows
        self.__state = []  ## state, see nextPositions

    def done(self):
        return len(self.__state) == self.__size

    def __iter__(self):
        return iter(nextPositions(self.__size, self.__state))

    def getState(self):
        return list(self.__state)

    def do(self, step):
        self.__state.append(step)

    def undo(self, step):
        self.__state.pop()


def queens_conjoin(n):
    """ liefert alle Loesungen des Damenproblems auf einem nxn-Schachbrett.

    Mit conjoin. Der absolute Wahnsinn. Idee:
    a) Die for-Schleife erzeugt einen Array gs von Generatoren g
    b) state ist global fuer alle g's. Dort steht die aktuelle Position
    c) gs[i] liefert - abhaengig von state - alle zulaessigen Positionen
       der i-ten Zeile
    """
    gs = []
    state = n * [None]
    for i in range(n):
        def g(i=i):
            for x in nextPositions(n, state[:i]):
                state[i] = x
                yield x

        gs.append(g)

    ##    return simple_conjoin(gs)
    return conjoin(gs)
##  return flat_conjoin(gs)
