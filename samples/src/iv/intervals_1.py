## trying to understand intervals
## js 8.6.04
## optimization by binary search
## js 26.6.04

from bisect import bisect_left, bisect_right
from operator import and_, or_

from fp.util import flip, oo, minusoo


def minClosure(bound1, bound2, closed1, closed2, op):
    """ liefert
        min(bound1, bound2) und
        closed1 or closed2 bzw. closed1 and closed2
        je nachdem, wo das Minimum angenommen wird. """
    if bound1 < bound2:
        return bound1, closed1
    elif bound1 == bound2:
        return bound1, op(closed1, closed2)
    else:
        return bound2, closed2


def maxClosure(bound1, bound2, closed1, closed2, op):
    """ liefert
        max(bound1, bound2) und
        closed1, closed2 bzw. closed1 and closed2
        je nachdem, wo das Maximum angenommen wird.
        op = and_ bzw. or_
    """
    if bound1 > bound2:
        return bound1, closed1
    elif bound1 == bound2:
        return bound1, op(closed1, closed2)
    else:
        return bound2, closed2


class Interval(object):
    """ Jedes Intervall hat eine linke und eine rechte Grenze.
        Es ist links offen oder abgeschlossen und rechts offen oder abgeschlossen.
        Es ist links beschraenkt oder unbeschraenkt (-oo) und
        rechts beschraenkt oder unbeschraenkt (oo).
        Das leere Interval wird dargestellt als [+oo, -oo]
        Das Universum ist (-oo, +oo)

        Folgende Operationen werden unterstuetzt:
        +v, -v                  (Ergebnis sind Intervall-Listen)
        v&w                     (Ergebnis ist Intervall)
        v|w, v-w, v^w           (Ergebnis sind Intervall-Listen)
        x in v
        v <, <=, ==, >=, > w    (Pruefung auf Teilintervall)
    """

    def __init__(self, leftBound=oo, rightBound=minusoo, leftClosed=True, rightClosed=False):
        self.leftBound = leftBound
        self.leftClosed = leftClosed
        self.rightBound = rightBound
        self.rightClosed = rightClosed

        if self.leftBound is -oo:
            self.leftClosed = False
        if self.rightBound is oo:
            self.rightClosed = False

        if self.leftBound > self.rightBound or \
                (self.leftBound == self.rightBound and \
                 not (self.leftClosed and self.rightClosed)):  ## empty interval
            self.leftBound = oo
            self.leftClosed = True
            self.rightBound = -oo
            self.rightClosed = True

    def closure(self):
        return Interval(self.leftBound, self.rightBound, True, True)

    def interior(self):
        return Interval(self.leftBound, self.rightBound, False, False)

    def touchesLeft(self, w):
        """ w : interval """
        if not isinstance(w, Interval):
            raise TypeError
        return self.rightBound == w.leftBound and \
               (self.rightClosed or w.leftClosed)

    touches = lambda self, w: self.touchesLeft(w) or w.touchesLeft(self)
    touchesRight = flip(touchesLeft)

    def __contains__(self, x):
        return self.leftBound < x < self.rightBound or \
               (self.leftBound == x and self.leftClosed) or \
               (self.rightBound == x and self.rightClosed)

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

        return (w.leftBound < self.leftBound or \
                (w.leftBound == self.leftBound and \
                 (w.leftClosed or not self.leftClosed))) and \
               (self.rightBound < w.rightBound or \
                (self.rightBound == w.rightBound and \
                 (not self.rightClosed or w.rightClosed)))

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

        leftBound, leftClosed = maxClosure(self.leftBound, w.leftBound, \
                                           self.leftClosed, w.leftClosed, and_)
        rightBound, rightClosed = minClosure(self.rightBound, w.rightBound, \
                                             self.rightClosed, w.rightClosed, and_)
        return Interval(leftBound, rightBound, leftClosed, rightClosed)

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
        return self.leftBound is not oo

    def __repr__(self):
        if not self:
            return '()'

        if self.leftClosed:
            leftbracket = '['
        else:
            leftbracket = '('
        if self.rightClosed:
            rightbracket = ']'
        else:
            rightbracket = ')'
        return leftbracket + `self.leftBound` + ', ' + `self.rightBound` + rightbracket


iv = Interval  ## Synonym fuer Interval, z.B.: iv(0, oo)
iv.emptyInterval = Interval()
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

    def __init__(self, vs=(), safe=False):
        if isinstance(vs, Interval):
            self.append(vs)
        elif isinstance(vs, (list, tuple)) and safe:
            list.__init__(self, vs)
        elif isinstance(vs, (list, tuple)) and not safe:
            for v in vs:
                self.append(v)
        else:
            raise TypeError

    def append(self, w):
        """ non empty intervals are inserted at the correct place """
        if not isinstance(w, Interval):
            raise TypeError
        if not w:
            return  ## w is empty; nothing to do

        ileft = bisect_left([v.rightBound for v in self], w.leftBound)
        iright = bisect_right([v.leftBound for v in self], w.rightBound) - 1

        ##        ts = [(i, v) for (i, v) in enumerate(self) if v&w or v.touches(w)]
        ##
        ##        if ts:      ## w cuts or touches at least one v in self
        ##                    ## ersetze alle v in ts durch ein grosses Intervall
        ##            il, vl = ts[0]      ## vl: leftmost interval to be eaten
        ##            ir, vr = ts[-1]     ## vr: rightmost interval to be eaten

        if ileft <= iright:
            vl = self[ileft]
            vr = self[iright]
            lb, lc = minClosure(w.leftBound, vl.leftBound, \
                                w.leftClosed, vl.leftClosed, or_)
            rb, rc = maxClosure(w.rightBound, vr.rightBound, \
                                w.rightClosed, vr.rightClosed, or_)

            ## eat all intervals from vl to vr included
            self[ileft:iright + 1] = [Interval(lb, rb, lc, rc)]

            ## w cuts or touches no v in self
        else:  ## i = leftmost interval w with w.rightBound <= v.leftBound
            i = bisect_left([v.leftBound for v in self], w.rightBound)
            list.insert(self, i, w)

    def closure(self):
        return Intervals([v.closure() for v in self])

    def interior(self):
        return Intervals([v.interior() for v in self], True)

    def __contains__(self, x):
        """ x ist entweder ein Intervall oder irgendwas.
            Im ersten Fall ist das Ergebnis True, wenn x Teilintervall von wenigstens
            einem (und damit genau einem) v in self ist.
            Im zweiten Fall ist das Ergebnis True, wenn x in mindestens einem v in self
            enthalten ist.
        """
        if (isinstance(x, Interval)):
            v = x
            x = x.leftBound
        else:  ## x is not an interval
            v = None

        ## i = index of leftmost interval v with x <= v.rightBound
        ## x is contained in the interval self[i] or in none them.
        i = bisect_left([w.rightBound for w in self], x)
        if i >= len(self):
            return false
        elif v is None:  ## x is not an interval
            return x in self[i]
        else:  ## v = x is an interval
            return v <= self[i]

    def __pos__(self):
        return self

    def __neg__(self):
        """ yields list of intervals complementary to self
            invariant:  v | -v == (-oo, +oo)
        """

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
