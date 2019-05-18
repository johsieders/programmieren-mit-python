## Integers over a prime p
## trying to understand the fields Fp

from operator import mul


class F(int):
    """ F represents the fields Fp (integers over p where p is prime)
        F ist abstract. Subclasses supply the prime self.p
    """

    def __coerce__(self, n):
        if not isinstance(n, (int)):
            raise TypeError('int required')
        elif not isinstance(n, type(self)):
            return self, type(self)(n % self.p)
        else:
            return self, n

    def __add__(self, n):
        self, n = coerce(self, n)
        return type(self)(int.__add__(self, n) % self.p)

    def __sub__(self, n):
        self, n = coerce(self, n)
        return type(self)(int.__sub__(self, n) % self.p)

    def __rsub__(self, n):
        self, n = coerce(self, n)
        return type(self)(int.__sub__(n, self) % self.p)

    def __mul__(self, n):
        self, n = coerce(self, n)
        return type(self)(int.__mul__(self, n) % self.p)

    def __invert__(self):
        return type(self)(int.__pow__(self, self.p - 2) % self.p)

    def __div__(self, n):
        self, n = coerce(self, n)
        return self * ~n

    def __rdiv__(self, n):
        self, n = coerce(self, n)
        return n * ~self

    def __pow__(self, n):
        if not isinstance(n, (int, long)):
            raise TypeError, 'int or long required'
        return reduce(mul, [self] * n, 1)

    __radd__, __rmul__ = __add__, __mul__


def makeFp(p):
    """ p must be prime.
        makeFp returns a subclass Fp of F
    """

    class Fp(F):
        pass

    Fp.p = p
    return Fp


if __name__ == '__main__':
    pass
