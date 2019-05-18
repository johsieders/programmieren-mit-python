## trying to understand more about intervals
## js 6.7.04


from bisect import bisect

from fp.util import flip, odd, even, oo


class IntervalAlgebra(object):
    def __init__(self, bounds=None, closed=None, leftBounded=True):
        if bounds is None:
            self.bounds = [-oo, oo]
        else:
            self.bounds = [-oo] + bounds + [oo]

        if closed is None:
            self.closed = [False, False]
        else:
            self.closed = closed[:]

        self.leftBounded = leftBounded

    def __neg__(self):
        return IntervalAlgebra(self.bounds, \
                               [not c for c in self.closed], not self.leftBound)

    def __pos__(self):
        return IntervalAlgebra(self.bounds, self.closed, self.leftBound)

    def isLeftBorder(self, i):
        """ bounds[i] is left border of an interval """
        return self.leftBounded and odd(i) or \
               not self.leftBounded and even(i)

    def rightBounded(self):
        return self.isLeftBorder(len(self.bounds))

    def bounded(self):
        return self.leftBounded and self.rightBounded()

    def __contains__(self, x):
        i = bisect(self.bounds, x) - 1  ## bounds[i] <= x < bounds[i+1]
        return self.isLeftBorder(i) and (self.closed[i] or self.bounds[i] < x)

    def __getitem__(self, i):
        """ returns i-th interval; supports slices """
        if self.leftBounded:
            i = 2 * i
        else:
            i = 2 * i + 1
        return Interval(self.bounds[i], self.bounds[i + 1], \
                        self.closed[i], self.closed[i + 1])

    def __delitem__(self, idx):
        """ deletes i-th intervall """
        pass

    def __len__(self):
        if self.bound():
            return sum([self.bounds[2 * i + 1] - self.bounds[2 * i] \
                        for i in range(len(self.bounds) / 2)])
        else:
            raise OverflowError

    def __nonzero__(self):
        return not self.leftBound or self.bounds

    def __le__(self, w):
        if not isinstance(w, IntervalAlgebra):
            raise TypeError

    def __lt__(self, w):
        return self <= ws and not self == ws

    def __eq__(self, w):
        return self <= ws and ws <= self

    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)

    def __ior__(self, w):
        if not isinstance(w, IntervalAlgebra):
            raise TypeError

    def __or__(self, w):
        result |= ws
        return result

    def __iand__(self, w):
        if not isinstance(w, IntervalAlgebra):
            raise TypeError

    def __and__(self, w):
        result &= w
        return result

    def __sub__(self, w):
        """ w: Intervals """
        return self & -ws

    def closure(self):
        pass

    def interior(self):
        pass

    def __repr__(self):
        pass


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

    def __init__(self, leftBound, rightBound, leftClosed, rightClosed):
        self.leftBound = leftBound
        self.leftClosed = leftClosed
        self.rightBound = rightBound
        self.rightClosed = rightClosed

    def __contains__(self, x):
        return self.leftBound < x < self.rightBound or \
               (self.leftBound == x and self.leftClosed) or \
               (self.rightBound == x and self.rightClosed)

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

##iv = Interval    ## Synonym fuer Interval, z.B.: iv(0, oo)
##iv.emptyInterval = Interval()
##iv.universe      = Interval(-oo, +oo)
