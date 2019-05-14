## trying to understand intervals
## js 8.6.04
## optimization by binary search
## js 26.6.04
## relaunch 21.11.04
## 26.12.04  ok 

from operator import add
from bisect import bisect_left, bisect_right
from functools import reduce

flip = lambda f: lambda x, y: f(y, x)      # flips args

def isInterval(v):
    """ v : list or tuple of length 2 """
    return isinstance(v, (tuple, list)) and len(v) == 2

def isEmptyInterval(v):
    """ v : list or tuple of length 2 """
    if not isInterval(v):
        raise TypeErrror

    return v[0] is not None and v[1] is not None and v[1] <= v[0]


class Vlist(list):
    """
    This class implements lists of non-empty intervals (vlists for short).

    An interval is a pair v of two Python objects:
    v[0] is the left bound, v[1] the right bound.

    If v[0] is None, the interval is left unbounded,
    if v[1] is None, the interval is right unbounded.

    The bounds are assumed to support comparisons.

    Each vlist is either empty, that is, it contains no intervals at all.
    Or it contains one or more non-empty disjoint intervals in ascending order.

    All intervals are left-closed and right-open. They can be leftbounded, rightbounded or both.

    Vlists are closed with respect to union (|), complement (-)
    and intersection. (&). They form a Boolean Algebra.

    This class implements the following operations (vs, ws are vlists)

    x in vs
    +vs, -vs
    vs|ws, vs&ws, vs-ws, vs^ws, vs|w, vs&w, vs-w, vs^w
    x in vs, v in vs
    vs <, <=, ==, >=, > ws
    """

    def __init__(self, *vs):
        """ vs: sequence of intervals """
        self.leftbounded = True       ## leftbounded as default
        for v in vs:
            self.append(v)

    def clone(self):
        result = Vlist()
        result[:] = self[:]
        result.leftbounded = self.leftbounded
        return result


    def outside(self, i):
        """ outside(i) == True <=> self[i] not in self """
        return (self.leftbounded + i) % 2

    def inside(self, i):
        """ inside(i) == True <=> self[i] in self """
        return not self.outside(i)

    def rightbounded(self):
        return self.outside(len(self))

    def sum(self):
        if self.leftbounded and self.rightbounded():
            return reduce(add, [v[1] - v[0] for v in self])
        else:
            raise OverflowError

    def __contains__(self, x):
        """ x : Interval or any object.
            Returns true iff x is contained in one of self's intervals
        """
        if isInterval(x):
            return x == self.intersect(x)
        else:
            return self.inside(bisect_right(self, x))


    def __pos__(self):
        return self


    def __neg__(self):
        """ Returns vlist complementary to self
            Invariant:  v | -v == (-oo, +oo)
        """
        result = self.clone()
        result.leftbounded = not self.leftbounded
        return result


    def append(self, v):
        """ v : interval
            Non empty intervals are inserted in the correct place.
            Returns None, changes self """

        if isEmptyInterval(v):      ## v is empty, nothing to do                                  
            return None

        ## where does the interval [v[0], v[1]) extend?     
        tmp = [0, len(self)]
        if v[0] is not None:
            tmp[0] = bisect_left(self, v[0])
        if v[1] is not None:
            tmp[1] = bisect_right(self, v[1])

            ## what about the bounds v[0] and v[1]?
        if v[0] is not None and self.outside(tmp[0]):
            head = [v[0]]
        else:
            head = []               ## forget v[0] if it's inside
        if v[1] is not None and self.outside(tmp[1]):
            tail = [v[1]]
        else:
            tail = []               ## forget v[1] if it's inside        

        ## set up union            
        self[tmp[0]:tmp[1]] = head + tail
        self.leftbounded = (v[0] is not None) and self.leftbounded


    def intersect(self, v):
        """ v : interval
            Returns elementwise intersection of self and v.
            Does not change self. """

        if isEmptyInterval(v):      ## v is empty, return empty interval            
            return Vlist()

        ## where does the interval [v[0], v[1]) extend?
        tmp = [0, len(self)]
        if v[0] is not None:        ## self[i] <= v[0] for i < tmp[0]
            tmp[0] = bisect_right(self, v[0])
        if v[1] is not None:        ## self[i] >= v[1] for i > tmp[1]
            tmp[1] = bisect_left(self, v[1])

        ## what about the bounds v[0] and v[1]?
        if v[0] is not None and self.inside(tmp[0]):
            head = [v[0]]
        else:
            head = []               ## forget v[0] if it's outside
        if v[1] is not None and self.inside(tmp[1]):
            tail = [v[1]]
        else:
            tail = []               ## forget v[1] if it's outside

        ## set up intersection
        result = Vlist()
        result[:] = head + self[tmp[0]:tmp[1]] + tail
        result.leftbounded = (v[0] is not None) or self.leftbounded
        return result


    def __ior__(self, vs):
        """ vs: vlist.
            Computes the elementwise union of self and vs.
            Each v in vs is appended to self.
            Changes self. """

        for v in vs:
            self.append(v)
        return self


    def __or__(self, vs):
        result = self.clone()
        result |= vs
        return result


    def __and__(self, vs):
        """ vs: vlist. Cool.
    Returns the elementwise intersection of self and vs.
    The resulting intervals are unioned. This is deMorgan's rule:
    (A | B | C) & (D | E) = ((A | B | C) & D) | ((A | B | C) & E)
    Does not change self. """

        if not isinstance(vs, Vlist):
            raise TypeError

        result = Vlist()
        result.leftbounded = self.leftbounded or vs.leftbounded
        for v in vs:
            result.extend(self.intersect(v)[:])
        return result


    def __sub__(self, vs):
        """ vs: vlist """
        return self & -vs

    def __xor__(self, vs):
        """ vs: vlist """
        return (self | vs) - (self & vs)

    def __le__(self, vs):
        """ vs: vlist
            Returns True iff each v in self is contained in vs """

        if not isinstance(vs, Vlist):
            raise TypeError

        for v in self:
            if not v in vs:
                return False
        return True

    def __eq__(self, vs):
        return list.__eq__(self, vs) and self.leftbounded == vs.leftbounded

    def __lt__(self, ws):
        return self <= ws and not self == ws

    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)


    def __iter__(self):
        if self.leftbounded:
            return chain(((None, False),), zip(self, cycle((True, False))))
        else:
            return chain(((None, True),), zip(self, cycle((False, True))))
        

    def __iter__XX(self):
        """ yields all intervals in self """

        def inner():
            if self.leftbounded:
                vs = self[:]
            else:
                vs = [None] + self[:]
            if not self.rightbounded():
                vs.append(None)
            vs = iter(vs)
            while True:
                v = next(vs)
                w = next(vs)
                yield v, w

        return inner()


    def __repr__(self):
        result = ''
        for v in self:
            result += '[' + repr(v[0]) + ', ' + repr(v[1]) + '), '
        return result[:-2]

iv = Vlist    
