## js 31.12.2003

from poly import Polynom
from rat import Rational



class RationalPolynom(Polynom):
    def zeroPolynom(self):
        return RationalPolynom([Rational(0, 1)])
    def unitPolynom(self, n):
        assert n >= 0, "n must not be negative"
        return RationalPolynom([0]*n + [1])
    def makePolynom(self, coefficients):
        return RationalPolynom(coefficients)
