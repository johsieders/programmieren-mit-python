## trying to understand intervals
## js 8.6.04
## optimization by binary search
## js 26.6.04
## relaunch 21.11.04

from fp.util import flip
from operator import add
from bisect import bisect_left, bisect_right

class MinusInfinity(object):
    def __cmp__(self, other):
        if isinstance(other, MinusInfinity):
            return 0
        else:
            return -1
        
    def __pos__(self):
        return self

    def __neg__(self):
        return oo
        
    def __repr__(self):
        return '-oo'


class PlusInfinity(object):
    def __cmp__(self, other):
        if isinstance(other, PlusInfinity):
            return 0
        else:
            return 1

    def __pos__(self):
        return self

    def __neg__(self):
        return minusoo
    
    def __repr__(self):
        return '+oo'

oo      = PlusInfinity()
minusoo = MinusInfinity()


def checkforinterval(v):
    """ v : list or tuple of length 2 """
    if isinstance(v, (tuple, list)) and len(v) == 2:
        pass
    else:
        raise TypeError


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

    def __init__(self, *vs):
        """ vs: sequence of pairs """
        self.bounds  = []               ## all bounds sorted
        for v in vs:
            self.append(v)

    def leftbound(self):
        return self.bounds[0] is not minusoo

    def rightbound(self):
        return self.bounds[-1] is not oo

    def valid(self, i):
        """ returns True iff b[i], b[i+1] is an interval """
        return (self.leftbound() and i%2) or \
               (not self.leftbound() and not i%2)
    
    def __len__(self):
        if not (self.leftbound() and self.rightbound()):
            raise OverfloError
        return reduce(add, [v[1] - v[0] for v in self])
    

    def append(self, v):            
        """ v : pair of comparable objects
            non empty intervals are inserted in the correct place """
        checkforinterval(v)
        if v[0] >= v[1]:   ## w is empty; nothing to do
            return          
                    ## ileft  = index of leftmost interval to be eaten
                    ## iright = index of leftmost interval not to be eaten
        ileft  = bisect_left(self.bounds, v[0])
        iright = bisect_right(self.bounds, v[1]) 
        
        if ileft < iright:                 
                    ## eat all intervals from ileft up to but excluding iright
            bleft  = min(v[0], self.bounds[ileft-1])
            if iright < len(self.bounds):
                bright = max(v[1], self.bounds[iright])
            else:
                bright = v[1]
            self.bounds[ileft-1:iright+1] = [bleft, bright]

                    ## w intersects no v in self; ileft == iright
        else:       ## ileft = leftmost interval v with v.rightBound < v.leftBound                  
            self.bounds.insert(ileft, v[1])
            self.bounds.insert(ileft, v[0])


    def __contains__(self, x):         
        """ x : any object.
            returns true iff x is contained in any of self's intervals
        """            
                    ## ix = index of leftmost interval v with x < v.rightBound
                    ## x is contained in the interval self[ix] or in none them.
        ix = bisect_right(self.bounds, x)
        return ix < len(self.bounds) and        \
               (self.leftbound() and ix%2) or   \
               (not self.leftbound() and not ix%2)


    def __pos__(self):
        return self


    def __neg__(self):  
        """ yields list of intervals complementary to self
            invariant:  v | -v == (-oo, +oo)
        """
        if self.leftbound():                  
            self.bounds.insert(0, minusoo)
        else:
            del self.bounds[0]

        if self.rightbound():
            self.bounds.append(oo)
        else:
            del self.bounds[-1]
    

    def __ior__(self, vs):
        """ vs may be Interval or Intervals.
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

    def __and__(self, ws):          ## TODO
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
            result.extend([v&w for v in self if v&w])   ## bisect!!
        return Intervals(result, True)
    

    def __sub__(self, ws):
        """ ws: Interval or Intervals. """
        return self & -ws

    def __xor__(self, ws):
        """ ws: Interval or Intervals. """        
        return (self|ws) - (self&ws)
    
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

    __ge__   = flip(__le__)
    __gt__   = flip(__lt__)


    def __iter__(self):
        """ yields all intervals in self """
        def inner():
            bounds = iter(self.bounds)
            while True:
                a = bounds.next()
                b = bounds.next()
                yield a, b
        return inner()

    
    def __repr__(self):
        if not self.bounds:
            return '[]'
        
        result = ''
        for v in self:
            result += '[' + repr(v[0]) + ', ' + repr(v[1]) + '), '           
        return result[:-2]