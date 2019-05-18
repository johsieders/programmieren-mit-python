# Polynome
# js, 25.05.01
# ueberarbeitung 29.12.03, 1.1.2004, 15.7.2004

from mathutil import flip, gcd


class Polynom(list):
    """
    p(x) = c[0]x**(n-1) + c[1]x**(n-2) + .. + c[n-2]x + c[n-1]
    no leading zeros
    any polynom has at least one coefficient.
    a polynom is zero iff its only coefficient is zero

    This class is intended for polynoms over any ring
    self.__zero = c[0] - c[0]
    coefficients support +, -, *, /, bool
    """

    def __init__(self, c, zero=None):
        """ c: sequence of coefficients
            leading zeros are discarded """
        assert len(c) > 0 or zero is not None
        if zero is not None:
            self.__zero = zero
        else:
            self.__zero = c[0] - c[0]
        i = 0
        while i < len(c) and not c[i]:
            i += 1
        list.__init__(self, c[i:])
        if len(self) == 0:
            self.append(self.__zero)

    def normalize(self):
        g = gcd(*self);
        for i in range(len(self)):
            self[i] /= g

    def degree(self):
        return len(self) - 1

    def __nonzero__(self):
        return len(self) > 1 or bool(self[0])

    def __coerce__(self, x):
        if isinstance(x, Polynom):
            return self, x
        elif isinstance(x, list) or isinstance(x, tuple):
            return self, Polynom(x)
        else:
            return self, Polynom([x])

    def __call__(self, x):
        return reduce(lambda a, b: x * a + b, self)

    #########################
    # arithmetic operations	#
    #########################

    def __neg__(self):
        return Polynom([-c for c in self], self.__zero)

    def __pos__(self):
        return Polynom(self, self.__zero)

    def __add__(self, p):
        s, q = coerce(self, p)
        if len(self) > len(q):
            a, b = self, q
        else:
            a, b = q, self
        result = list(a)
        for i in range(1, len(b) + 1):
            result[-i] += b[-i]
        return Polynom(result, self.__zero)

    def __sub__(self, p):
        return self + -p

    def __mul__(self, p):
        s, q = coerce(self, p)
        result = [self.__zero] * (len(self) + len(q) - 1)
        for i in range(len(self)):
            for j in range(len(q)):
                result[i + j] += self[i] * q[j]
        return Polynom(result, self.__zero)

    def __divmod__(self, p):
        """ q = quotient
            r = remainder
            invariant: self = p * q + r """
        s, t = coerce(self, p)
        q = []
        r = list(self)
        while len(r) >= len(t):
            c = r[0] / t[0]  ## quotient of highest coefficients
            q.append(c)
            for i in range(len(t)):
                r[i] -= c * t[i]
            i = 0
            while i < len(r) and not r[i]: i += 1
            r = r[i:]  ## discard leading zeros
        return Polynom(q, self.__zero), Polynom(r, self.__zero)

    ##    recursive implementation
    ##    def __divmod__(self, p, q=None):
    ##        if not q:
    ##            q = Polynom([self.__zero])
    ##        n = self.degree() - p.degree()
    ##        if n < 0:
    ##            return [q, self]
    ##        a = self[self.degree()]/p[p.degree()]
    ##        if not a:
    ##            return [q, self]
    ##        r = self - a*Polynom(n)*p
    ##        q = q + a*Polynom(n)
    ##        return r.__divmod__(p, q)

    def __div__(self, p):
        return divmod(self, p)[0]

    def __mod__(self, p):
        return divmod(self, p)[1]

    def __pow__(self, n):
        ## kein coerce!!
        from operator import mul
        assert isinstance(n, int) or isinstance(n, long)
        if not n:
            return Polynom([self.__zero])
        else:
            return reduce(mul, [self] * n)

    def __cmp__(self, p):
        pass

    # make operators with reversed operands
    __radd__, __rmul__ = __add__, __mul__

    __rsub__, __rdiv__, __rmod__, __rcmp__ = \
        [flip(m) for m in [__sub__, __div__, __mod__, __cmp__]]

## end of class Polynom
