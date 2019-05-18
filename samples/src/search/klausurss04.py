## Klausur 8.7.04

from itertools import count, imap

from search import SearchProblem

## Aufgabe 1
## kurze Loesung
histogram = lambda m: dict([[k, m.count(k)] for k in m])


## lange Loesung
def histogram1(xs):
    result = {}
    for x in xs:
        if x not in result:
            result[x] = 1
        else:
            result[x] += 1
    return result


## Aufgabe 2
## kurze Loesung
transpose = lambda m: zip(*m)

## lange Loesung
transpose1 = lambda m: map(None, *m)


## Aufgabe 3
## a)
class A(object): pass


class B(object): pass


class C(A, B): pass


class D(B, object): pass


class E(C, D): pass


## b)  (mit O = object)
## A.mro = AO
## B.mro = BO
## C.mro = C + merge(AO, BO, AB) = CABO
## D.mro = D + merge(BO, O, BO) = DBO
## E.mro = E + merge(CABO, DBO, CD)
##       = EC + merge(ABO, DBO, D)
##       = ECA + merge(BO, DBO, D)
##       = ECAD + merge(BO, BO) = ECADBO

## c) Der C3-Algorithmus ist monoton. Das bedeutet: Ist C Unterklasse
## der Klassen A und B, dann gilt fuer jede Unterklasse D von C:
## Ist A Vorgaenger von B in C.mro(), dann gilt dies auch in D.mro().

## d)
## Der Aufruf von super in der Klasse C gelangt zum Nachfolger von C in C.mro().
## Aufruf von foo aus der Klasse C heraus durch:
##      super(C, self).foo()


## Aufgabe 4
## a)
def g7():
    yield 1
    current = 7
    while True:
        yield current
        current += 7


## b)
def gf(f):
    current = 1
    while True:
        yield current
        current = f(current)


## c)
## kurze Loesung
gop = imap


## lange Loesung
def gop1(op, i, j):
    while True:
        yield op(i.next(), j.next())


## d)
def gq():
    for a in count(1):
        for b in range(1, a + 1):
            yield a ** 2 + b ** 2


## Aufgabe 5
class PermutationProblem(SearchProblem):
    def __init__(self, xs):
        self.__xs = list(xs)
        self.__state = []

    def gotSolution(self):
        return len(self.__state) == len(self.__xs)

    def __iter__(self):
        return iter(Set(self.__xs) - Set(self.__state))

    def getState(self):
        return list(self.__state)

    def doStep(self, step):
        self.__state.append(step)

    def undoStep(self, step):
        self.__state.pop()

    ## Aufgabe 6


class talist(list):
    def __init__(self, seq=[]):
        list.__init__(self, seq)
        self.before = seq[:]

    def rollback(self):
        self[:] = self.before

    def commit(self):
        self.before[:] = self

    ## alle anderen Methoden kommen von list
