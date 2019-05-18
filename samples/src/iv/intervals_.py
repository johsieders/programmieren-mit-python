## trying to understand intervals
## js 9/5/2004
## new trial: kiss

from fp.util import flip, oo, minusoo


class Interval(object):
    """ Intervals have a left border a and a right border b.
        We only consider left closed intervals:
        they contain the left border but not the right one.
        Intervals are empty iff a >= b.
        Intervals a left bounded or left unbounded (a is -oo) 
        and they are right bounded or unbounded (b is oo)
        The universe is (-oo, oo). The following oerations are supported:

        +v, -v                  (returns list of intervals)
        v&w                     (returns interval)
        v|w, v-w, v^w           (returns list of intervals)
        x in v					(x contained in v)
        v <, <=, ==, >=, > w    (check for subinterval)
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def touchesLeft(self, w):
        if not isinstance(w, Interval):
            raise TypeError
        return self.b == w.b

    touches = lambda self, w: self.touchesLeft(w) or w.touchesLeft(self)

    def __contains__(self, x):
        return self.a <= x < self.b

    def __len__(self):
        if not self:
            return 0
        elif self.a is minusoo or self.b is oo:
            raise OverflowError
        else:
            return self.b - self.a

    def __le__(self, w):
        if not isinstance(w, Interval):
            raise TypeError

        return not w or \
               (self.a <= w.a < self.b and \
                self.a <= w.b <= self.b)

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
        return Interval(max(self.a, w.a), min(self.b, w.b))

    def __sub__(self, w):
        """ w: Interval or Intervals"""
        return +self & -w

    def __or__(self, w):
        """ w: Interval or Intervals"""
        return +self | +w

    def __xor__(self, w):
        """ w may be Interval or Intervals"""
        return (self | w) - (self & w)

    def __nonzero__(self):
        return self.a < self.b

    def __repr__(self):
        if not self:
            return '[)'
        return '[' + repr(self.a) + ', ' + repr(self.b) + ')'


iv = Interval  ## Synonym fuer Interval, z.B.: iv(0, oo)
iv.emptyInterval = Interval(0, 0)
iv.universe = Interval(-oo, +oo)


class Intervals(list):
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

    def __init__(self, v):
        if not isinstance(v, Interval):
            raise ValueError
        list.append(self, v)

    def append(self, w):
        """ nichtleere Intervalle werden korrekt eingefuegt """
        if not isinstance(w, Interval):
            raise TypeError
        if not w:
            return  ## nothing to do
        else:
            vs = [v for v in self if v & w]
            self[self.index(vs[0]):self.index[vs[-1]] + 1] = w

    def __contains__(self, x):
        """ x ist entweder ein Intervall oder irgendwas.
            Im ersten Fall ist das Ergebnis True, wenn x Teilintervall von wenigstens
            einem (und damit genau einem) v in self ist.
            Im zweiten Fall ist das Ergebnis True, wenn x in mindestens einem v in self
            enthalten ist.
        """

        if isinstance(x, Interval):
            return True in [x <= v for v in self]
        else:
            return True in [x in v for v in self]

    def __pos__(self):
        return self

    def __neg__(self):
        """ liefert die Liste der zu self komplementaeren Intervalle"""

        result = []
        wLeftBound = -oo
        wLeftClosed = False

        for v in self:
            wRightBound = v.leftBound
            wRightClosed = not v.leftClosed
            w = Interval(wLeftBound, wRightBound, wLeftClosed, wRightClosed)
            result.append(w)
            wLeftBound = v.rightBound
            wLeftClosed = not v.rightClosed

        wRightBound = oo
        wRightClosed = False
        w = Interval(wLeftBound, wRightBound, wLeftClosed, wRightClosed)
        result.append(w)
        return Intervals(result, True)

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
        result = Intervals(self, True)
        result |= ws
        return result

    def __and__(self, ws):
        """ ws: Interval or Intervals. Cool.
            For each w in ws you construct Intervals [v&w for v in self if v&w]
            D.h.: Jedes v in self wird mit w geschnitten; Ergebnis sind
            die nicht-leeren Schnittintervalle.
            These Intervals are unioned. This is deMorgan's rule:
            (A | B | C) & (D | E) = ((A | B | C) & D) | ((A | B | C) & E)
        """
        self, ws = coerce(self, ws)
        result = []
        for w in ws:
            result.extend([v & w for v in self if v & w])
        return Intervals(result)

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
