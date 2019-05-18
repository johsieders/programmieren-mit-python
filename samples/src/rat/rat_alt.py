## Rationale Zahlen
## js 1.1.2004

from mathutil import flip, gcd

_THRESHOLD = 5


class Rational:
    """
    rational numbers defined on any euclidian ring
    (e.g. integer, polynomials)
    assume +, -, *,/, %, <, bool
    denominator may never be zero, so let:
    zero = denominator - denominator
    one  = denominator / denominator
    normalization after _THRESHOLD generations
    Rationals are callable iff numerator and denominator
    are callable
    """

    def __init__(self, first, second, \
                 zero=None, one=None, generation=_THRESHOLD):
        if isinstance(first, Rational) or isinstance(second, Rational):
            q = first / second
            assert isinstance(tmp, Rational)
            self.__numerator = q.__numerator
            self.__denominator = q.__denominator
        else:
            self.__numerator = first
            self.__denominator = second
        self.__generation = generation - 1
        if zero:
            self.__zero = zero
        else:
            self.__zero = self.__denominator - self.__denominator
        if one:
            self.__one = one
        else:
            self.__one = self.__denominator / self.__denominator
        if self.__generation < 0:
            self.norm()

    def __coerce__(self, x):
        if isinstance(x, Rational):
            return self, x
        else:
            return self, Rational(x, self.__one)

    def __nonzero__(self):
        return bool(self.__numerator)

    def norm(self):
        if self.__denominator < self.__zero:
            self.__numerator = -self.__numerator
            self.__denominator = -self.__denominator
        g = gcd(self.__numerator, self.__denominator)
        if g != self.__one:
            self.__numerator /= g
            self.__denominator /= g
        self.__generation = _THRESHOLD

    def normalized(self):
        return self.__generation == _THRESHOLD

    def __call__(self, x):
        return Rational(self.__numerator(x), self.__denominator(x))

    def __float__(self):
        return float(self.__numerator) / float(self.__denominator)

    def __int__(self):
        return int(float(self))

    def __long__(self):
        return long(float(self))

    def __abs__(self):
        return Rational(abs(self.__numerator), self.__denominator, \
                        self.__zero, self.__one, self.__generation)

    def __neg__(self):
        return Rational(-self.__numerator, self.__denominator, \
                        self.__zero, self.__one, self.__generation)

    def __pos__(self):
        return Rational(self.__numerator, self.__denominator, \
                        self.__zero, self.__one, self.__generation)

    def __invert__(self):
        return Rational(self.__denominator, self.__numerator, \
                        self.__zero, self.__one, self.__generation)

    def __repr__(self):
        if not self.normalized(): self.norm()
        return `self.__numerator` + '/' + `self.__denominator`

    def __add__(self, r):
        num = self.__numerator * r.__denominator + self.__denominator * r.__numerator
        denom = self.__denominator * r.__denominator
        return Rational(num, denom, self.__zero, self.__one, self.__generation)

    def __sub__(self, r):
        return self + -r

    def __mul__(self, r):
        num = self.__numerator * r.__numerator
        denom = self.__denominator * r.__denominator
        return Rational(num, denom, self.__zero, self.__one, self.__generation)

    def __div__(self, r):
        return self * ~r

    def __mod__(self, r):
        return self.__zero

    def __cmp__(self, r):
        return cmp(self.__numerator * r.__denominator - \
                   self.__denominator * r.__numerator, self.__zero)

    # make operators with reversed operands
    __radd__, __rmul__ = __add__, __mul__

    __rsub__, __rdiv__, __rmod__ = \
        map(flip, [__sub__, __div__, __mod__])

    ## end of class Rational
