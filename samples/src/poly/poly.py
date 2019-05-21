# Polynome
# js, 25.05.01
# ueberarbeitung 29.12.03, 1.1.2004, 15.7.2004, 9.8.2004
# Portierung nach 3.6 21.5.2019

from functools import reduce

flip = lambda f: lambda x, y: f(y, x)  # flips args


class Polynom(list):
    """
    p(x) = c[0] + c[1]x + c[2]x**2 + .. + c[n-2]x**(n-2) + c[n-1]x**(n-1)
    no trailing zeros
    any polynom has at least one coefficient.
    a polynom is zero iff its only coefficient is zero

    This class is intended for polynoms over any field
    self.__zero = cs[0] - cs[0]
    coefficients must support +, -, *, /, bool
    """

    def __init__(self, cs):
        """ cs: sequence of coefficients
            trailing zeros are discarded """
        try:                            # test for iterable
            iter(cs)
        except TypeError:
            cs = [cs]                   # make cs iterable

        if len(cs) == 0:
            raise(ValueError, 'no coefficients')

        self.__zero = cs[0] - cs[0]
        i = len(cs) - 1
        while i > 0 and not cs[i]:
            i -= 1
        super(Polynom, self).__init__(cs[:i + 1])

    def degree(self):
        return len(self) - 1

    def __nonzero__(self):
        return bool(self[-1])

    def __call__(self, x):
        tmp = list(self)
        tmp.reverse()
        return reduce(lambda a, b: x * a + b, tmp)

    #########################
    # arithmetic operations	#
    #########################

    def __neg__(self):
        return Polynom([-c for c in self])

    def __pos__(self):
        return Polynom(self)

    def __add__(self, p):
        if type(p) is not Polynom:
            p = Polynom(p)
        if len(self) > len(p):
            a, b = self, p
        else:
            a, b = p, self
        result = list(a)                # a is at least as long as b
        for i, c in enumerate(b):
            result[i] += c
        return Polynom(result)

    def __sub__(self, p):
        return self + -p

    def __mul__(self, p):
        if type(p) is not Polynom:
            p = Polynom(p)
        result = [self.__zero] * (len(self) + len(p) - 1)
        for i in range(len(self)):
            for j in range(len(p)):
                result[i + j] += self[i] * p[j]
        return Polynom(result)

    def __divmod__(self, p):
        """ q = quotient
            r = remainder
            invariant: self = p * q + r """
        p = Polynom(p)
        q = []
        r = list(self)
        while len(r) >= len(p):
            c = r[-1] / p[-1]       # quotient of highest coefficients
            q.append(c)
            for i in range(-len(p), 0):
                r[i] -= c * p[i]
            del r[-1]               # discard highest coefficient

        q.reverse()
        if len(q) == 0:
            q.append(self.__zero)
        if len(r) == 0:
            r.append(self.__zero)
        return Polynom(q), Polynom(r)

    def __mod__(self, p):
        return divmod(self, p)[1]

    def __div__(self, p):
        return divmod(self, p)[0]

    def __pow__(self, n):
        from operator import mul
        if type(n) is not int:
            raise TypeError
        if n == 0:
            return Polynom([self.__zero])
        else:
            return reduce(mul, [self] * n)

    # make operators with reversed operands
    __radd__, __rmul__ = __add__, __mul__
    __rsub__, __rdiv__, __rmod__ = [flip(m) for m in [__sub__, __div__, __mod__]]


## end of class Polynom

p = Polynom([-2, 2] * 30)
if __name__ == '__main__':
    p = Polynom([1,1,1])
    q = p + 3
    print(q)
    q = p - 3
    print(q)
    q = p*5
    print (q)
    q = p(p)
    print(q)
    # from timeit import *
    # t = Timer('p(7543.0)', 'from poly import p')
    # t.repeat(3, 10000)
