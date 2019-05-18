## trying to understand intervals
## js 8.6.04
## optimization by binary search
## js 26.6.04
## relaunch 21.11.04

from bisect import bisect_left, bisect_right

from fp.util import flip, oo, minusoo


class Interval(object):
    """ Jedes Intervall hat eine linke und eine rechte Grenze.
        Es ist links abgeschlossen und rechts offen.
        Es ist links beschraenkt oder unbeschraenkt (-oo) und
        rechts beschraenkt oder unbeschraenkt (oo).
        Das leere Interval wird dargestellt als [+oo, -oo)
        Das Universum ist (-oo, +oo)

        Folgende Operationen werden unterstuetzt:
        +v, -v                  (Ergebnis sind Intervall-Listen)
        v&w                     (Ergebnis ist Intervall)
        v|w, v-w, v^w           (Ergebnis sind Intervall-Listen)
        x in v
        v <, <=, ==, >=, > w    (Pruefung auf Teilintervall)
    """

    def __init__(self, leftBound=oo, rightBound=minusoo):
        self.leftBound = leftBound
        self.rightBound = rightBound

        if self.leftBound >= self.rightBound:  ## empty interval
            self.leftBound = oo
            self.rightBound = minusoo

    def __contains__(self, x):
        return self.leftBound <= x < self.rightBound

    def __len__(self):
        if not self:
            return 0
        elif self.leftBound == minusoo or self.rightBound == oo:
            raise OverflowError
        else:
            return self.rightBound - self.leftBound

    def __le__(self, w):
        if not isinstance(w, Interval):
            raise TypeError

        return w.leftBound <= self.leftBound and \
               self.rightBound <= w.rightBound

    def __eq__(self, w):
        return self <= w and w <= self

    def __lt__(self, w):
        return self <= w and not self == w

    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)

    def __pos__(self):
        return Intervals(self)

    def __neg__(self):
        return -Intervals(self)

    def __and__(self, w):
        """ w: Interval or Intervals"""
        if isinstance(w, Intervals):
            return w & self

        leftBound = max(self.leftBound, w.leftBound)
        rightBound = min(self.rightBound, w.rightBound)
        return Interval(leftBound, rightBound)

    def __sub__(self, w):
        """ w: Interval or Intervals"""
        return +self & -w

    def __or__(self, w):
        """ w: Interval or Intervals"""
        return +self | +w

    def __xor__(self, w):
        """ w: Interval or Intervals"""
        return (self | w) - (self & w)

    def __nonzero__(self):
        return self.leftBound is not oo

    def __repr__(self):
        if not self:
            return '()'

        return '[' + repr(self.leftBound) + ', ' + repr(self.rightBound) + ')'


iv = Interval  ## Synonym fuer Interval, z.B.: iv(0, oo)
iv.emptyInterval = Interval()
iv.universe = Interval(-oo, +oo)


class Intervals(object):
    """ Jede Intervall-Liste ist entweder leer oder sie enthaelt
        nichtleere disjunkte Intervalle aufsteigend sortiert.

        Intervall-Listen sind abgeschlossen gegenueber Vereinigung (|),
        Komplement (-) und Durchschnitt (&). Sie bilden eine Boolsche Algebra.

        Folgende Operationen werden unterstuetzt
        (v, w sind Intervalle; vs, ws sind Intervall-Listen):
        +vs, -vs
        vs|ws, vs&ws, vs-ws, vs^ws, vs|w, vs&w, vs-w, vs^w
        x in vs, v in vs
        vs <, <=, ==, >=, > ws
        """

    def __coerce__(self, other):
        if isinstance(other, Intervals):
            return self, other
        if isinstance(other, Interval):
            return self, +other
        else:
            raise TypeError

    def __init__(self, *vs):
        self.leftBounds = []  ## sorted
        self.rightBounds = []  ## sorted
        for v in vs:
            self.append(v)

    def clone(self):
        result = Intervals()
        result.leftBounds = self.leftBounds[:]
        result.rightBounds = self.rightBounds[:]
        return result

    def __len__(self):
        return len(self.leftBounds)

    def append(self, w):
        """ non empty intervals are inserted in the correct place """
        if not isinstance(w, Interval):
            raise TypeError
        if not w:  ## w is empty; nothing to do
            return
            ## ileft  = index of leftmost interval to be eaten
            ## iright = index of leftmost interval not to be eaten
        ileft = bisect_right(self.rightBounds, w.leftBound)
        iright = bisect_left(self.leftBounds, w.rightBound)

        if ileft < iright:
            ## eat all intervals from ileft up to but excluding iright
            self.leftBounds[ileft:iright] = [min(w.leftBound, self.leftBounds[ileft])]
            self.rightBounds[ileft:iright] = [max(w.rightBound, self.rightBounds[iright - 1])]

            ## w intersects no v in self; ileft == iright
        else:  ## ileft = leftmost interval w with w.rightBound < v.leftBound
            self.leftBounds.insert(ileft, w.leftBound)
            self.rightBounds.insert(ileft, w.rightBound)

    def __contains__(self, x):
        """ x ist entweder ein Intervall oder irgendwas.
            Im ersten Fall ist das Ergebnis True, wenn x Teilintervall von wenigstens
            einem (und damit genau einem) v in self ist.
            Im zweiten Fall ist das Ergebnis True, wenn x in mindestens einem v in self
            enthalten ist.
        """
        if isinstance(x, Interval):
            v = x
            x = x.leftBound
        else:  ## x is not an interval
            v = None

            ## ix = index of leftmost interval v with x < v.rightBound
            ## x is contained in the interval self[ix] or in none them.
        ix = bisect_right(self.rightBounds, x)
        if ix >= len(self):
            return False
        elif v is None:  ## x is not an interval
            return x >= self.leftBounds[ix]
        else:  ## v = x is an interval
            return v <= self[ix]

    def __pos__(self):
        return self

    def __neg__(self):
        """ yields list of intervals complementary to self
            invariant:  v | -v == (-oo, +oo)
        """
        result = Intervals()
        if self.leftBounds[0] is minusoo:
            result.rightBounds = self.leftBounds[1:]
        else:
            result.rightBounds = self.leftBounds + [oo]

        if self.rightBounds[-1] is oo:
            result.leftBounds = self.rightBounds[:-1]
        else:
            result.leftBounds = [minusoo] + self.rightBounds

        return result

    def __ior__(self, ws):
        """ ws may be Interval or Intervals.
            __ior__ liefert die elementweise Vereinigung von self und ws:
            Jedes w in ws wird zu self hinzugefuegt.
        """
        self, ws = coerce(self, ws)
        for w in ws:
            self.append(w)
        return self

    def __or__(self, ws):
        result = self.clone()
        result |= ws
        return result

    def intersect(self, v):
        """ v : interval """
        if not isinstance(v, Interval):
            raise TypeError

        return self

    def __and__(self, ws):  ## TODO
        """ ws: Interval or Intervals. Cool.
            For each w in ws we construct the intervals [v&w for v in self if v&w]
            D.h.: Jedes v in self wird mit w geschnitten; Ergebnis sind
            die nicht-leeren Schnittintervalle.
            These Intervals are unioned. This is deMorgan's rule:
            (A | B | C) & (D | E) = ((A | B | C) & D) | ((A | B | C) & E)
        """
        self, ws = coerce(self, ws)
        result = []
        for w in ws:
            result.extend([v & w for v in self if v & w])  ## bisect!!
        return Intervals(result, True)

    def __sub__(self, ws):
        """ ws: Interval or Intervals. """
        return self & -ws

    def __xor__(self, ws):
        """ ws: Interval or Intervals. """
        return (self | ws) - (self & ws)

    def __le__(self, ws):
        """ ws: Intervals.
            Das Ergebnis ist True, wenn jedes v in self in wenigstens
            einem Intervall von ws enthalten ist.
        """
        if not isinstance(ws, Intervals):
            raise TypeError
        for v in self:
            if not v in ws:
                return False
        return True

    def __eq__(self, ws):
        return self <= ws and ws <= self

    def __lt__(self, ws):
        return self <= ws and not self == ws

    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)

    def __iter__(self):
        """ yields all intervals in self """

        def tmp():
            for a, b in zip(self.leftBounds, self.rightBounds):
                yield Interval(a, b)

        return tmp()

    def __repr__(self):
        if not self:
            return '[]'

        result = '['
        for v in self:
            result += repr(v) + ', '
        result = result[:-2] + ']'
        return result
