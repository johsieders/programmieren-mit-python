## Rationale Zahlen
## js 15.7. 2004
## Typkonzept komplett neu
## Idee: so einfach wie moeglich

def gcd(a, b):  #return gcd of a and b
    while b:
        a, b = b, a%b 
    return a

def flip(f):
    return lambda x, y : f(y,x)


class Rational(object):
    """
    rational numbers defined on an euclidian ring
    (e.g. integer, polynomials, series)
    assume +, -, *,/, %, <, bool
    denominator may never be zero, so let
    zero = denominator - denominator
    one  = denominator / denominator
    Rationals are callable iff numerator and denominator are callable
    """

    def __init__(self, first=0, second=1, zero=None, one=None, normalized=False):
        first, second = coerce(first, second)
        if zero is not None:
            self.__zero = zero 
        else:
            self.__zero = second - second
        if one is not None:
            self.__one = one
        else:
            self.__one = second / second        ## second must never be zero

        if isinstance(first, Rational):
            aux = first / second
            self.__numerator   = aux.__numerator
            self.__denominator = aux.__denominator
            normalized = True
        else:
            self.__numerator   = first          ## zaehler
            self.__denominator = second         ## nenner
            
        if not normalized:
            self.normalize()
            
    def numerator(self):
        return self.__numerator                      

    def denominator(self):
        return self.__denominator
 
    def __coerce__(self, x):
        if isinstance(x, Rational):
            return self, x
        elif isinstance(x, float):
            return float(self), x
        else:
            return self, Rational(x)

    def __nonzero__(self):
        return bool(self.__numerator)

    def normalize(self):
        if self.__denominator < self.__zero:
            self.__numerator   = -self.__numerator
            self.__denominator = -self.__denominator
        g = gcd(self.__numerator, self.__denominator)
        if g != self.__one:
            self.__numerator   /= g
            self.__denominator /= g

    def __call__(self, x):
        return Rational(self.__numerator(x), self.__denominator(x))
    
    def __float__(self):
        return float(self.__numerator)/float(self.__denominator)

    def __int__(self):
        return int(float(self))
        
    def __long__(self):
        return long(float(self))

    def __abs__(self):
        return Rational(abs(self.__numerator), self.__denominator, \
                        self.__zero, self.__one, True)

    def __neg__(self):
        return Rational(-self.__numerator, self.__denominator, \
                        self.__zero, self.__one, True)
        
    def __pos__(self):
        return Rational(self.__numerator, self.__denominator, \
                        self.__zero, self.__one, True)
            
    def __invert__(self):
        return Rational(self.__denominator, self.__numerator, \
                        self.__zero, self.__one)

    def __repr__(self):
        return repr(self.__numerator) + '/' + repr(self.__denominator)

    def __add__(self, r):
        s, t = coerce(self, r)
        if s is not self:
            return s + t
        else:
            num   = self.__numerator * t.__denominator + self.__denominator * t.__numerator
            denom = self.__denominator * t.__denominator
            return Rational(num, denom, self.__zero, self.__one)

    def __sub__(self, r):
        return self + -r

    def __mul__(self, r):
        s, t = coerce(self, r)
        if s is not self:
            return s * t
        else:
            num   = self.__numerator * t.__numerator
            denom = self.__denominator * t.__denominator
            return Rational(num, denom, self.__zero, self.__one)
    
    def __div__(self, r):
        return self * ~r

    def __mod__(self, r):
        return self.__zero

    def __divmod__(self, r):
        return self/r, self.__zero

    def __cmp__(self, r):
        s, t = coerce(self, r)
        return cmp(self.__numerator * t.__denominator - \
               self.__denominator * t.__numerator, self.__zero)

    # make operators with reversed operands
    __radd__, __rmul__ = __add__, __mul__

    __rsub__, __rdiv__, __rmod__, __rcmp__=   \
                [flip(m) for m in [__sub__, __div__, __mod__, __cmp__]]

    ## end of class Rational

if __name__ == '__main__':
    a = Rational(0)
    b = Rational(1)
    a/b