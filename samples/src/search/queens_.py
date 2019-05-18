## diverse Versuche zu den Queens
## js 10.8.02
## bubenorbis

from test.test_generators import conjoin


## from queens import nextRow


def nextPositions(n, currentPosition):
    """ liefert currentPosition ergaenzt um die Menge der sicheren Positionen
        in der naechsten Zeile.
    
        Beispiel: currentPosition = [3, 0] bedeutet:
        In Zeile 0 steht eine Koenigin auf Position 3
        in Zeile 1 steht eine Koenigin auf Position 0
        Sicher sind in Zeile 2 die Positionen 2 und 4
        Ergebnis mit n = 5: [[3, 0, 2], [3, 0, 4]]
    """
    return [currentPosition + [i] for i in nextRow(n, currentPosition)]


def queens1(n):
    """ liefert alle Loesungen des Damenproblems auf einem nxn-Schachbrett.

    Vorwaerts ohne Generator.    
    Idee: _queens(q, result) ermittelt alle von der Position q ausgehende Loesungen
    und fuegt diese zu result dazu.    
    """

    def _queens(q, result):
        if len(q) >= n:
            result.append(q)
        else:
            for p in nextPositions(n, q):
                _queens(p, result)

        return result

    return _queens([], [])


def queens2(n):
    """ liefert alle Loesungen des Damenproblems auf einem nxn-Schachbrett

    Vorwaerts mit Generator.    
    Idee: _queens(q) ermittelt alle Loesungen ausgehend von q und gibt sie per
    yield zurueck. Somit ist _queens(q) ein Iterator ueber alle von q ausgehende
    Loesungen  
    """

    def _queens(q):
        if len(q) >= n:
            yield q
        else:
            for p in nextPositions(n, q):
                for s in _queens(p):
                    yield s

    for s in _queens([]):
        yield s


def queens3(n):
    """ liefert alle Loesungen des Damenproblems auf einem nxn-Schachbrett

    Backward ohne Generator
    Idee: _queens(k) liefert alle Teilloesungen des Damenproblems mit k besetzten
    Reihen. _queens(k) ruft rekursiv _queens(k - 1)
    """

    def _queens(k):
        if k == 0:
            return [[]]

        result = []
        for q in _queens(k - 1):
            for p in nextPositions(n, q):
                result.append(p)

        return result

    return _queens(n)


##########################################
############## conjoin ###################
##########################################

# aus test_generators
# do not touch
def simple_conjoin(gs):
    def gen(i, values):
        if i >= len(gs):
            yield values
        else:
            for values[i] in gs[i]():
                for x in gen(i + 1, values):
                    yield x

    for x in gen(0, [None] * len(gs)):
        yield x


def queens4(n):
    """ liefert alle Loesungen des Damenproblems auf einem nxn-Schachbrett.

    Mit conjoin. Der absolute Wahnsinn.
    Idee:
    a) Die for-Schleife erzeugt einen Array gs von Generatoren g
    b) currentPosition ist global fuer alle g's. Dort steht die aktuelle Position
    c) gs[i] liefert - abhaengig von currentPosition - alle zulaessigen Positionen
       der i-ten Zeile
    """
    currentPosition = [None] * n
    gs = []
    for i in range(n):
        def g(i=i):
            for j in nextRow(n, currentPosition[:i]):
                currentPosition[i] = j
                yield j

        gs.append(g)

    ##  cj = simple_conjoin
    cj = conjoin
    ##  cj = flat_conjoin
    for s in cj(gs):
        yield s


def permutations(seq):
    gs = []
    current = len(seq) * [None]

    for i in range(len(seq)):
        def g(i=i):
            for x in seq:
                if x not in current[:i]:
                    current[i] = x
                    yield x

        gs.append(g)

    ##  cj = simple_conjoin
    cj = conjoin
    ##  cj = flat_conjoin
    for s in cj(gs):
        yield s
