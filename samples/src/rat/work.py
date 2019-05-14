
from poly import *
from rat import *


if __name__ == '__main__':
        print
        r = map(Rational, range(20), 20*[1])
        
##        p = Polynom((r[1], r[0], -r[1]))  ## (x - 1)(x + 1)
##        q = Polynom((r[1], -r[1]))        ## x - 1
##        rr = Rational(p,q)   
##        rr.norm()     ## rr(x) = x+1        
##        print rr
##
##        p = Polynom((r[1],))             ## 1
##        q = Polynom((r[1], r[0], r[1]))  ## x**2 +1
##        rr = Rational(p,q)   
##        rr.norm()               ## rr(x) = 1/(x**2 + 1)
##        print rr
##        print map(rr, range(-5, 5))

        p = Polynom((r[1], r[0], -r[16])) ## x**2-16
        q = Polynom((r[1], r[8], r[16]))  ## x**2 +8x+16
        g = gcd(p, q)
        rr = Rational(p,q)   
        rr.norm()               ## rr(x) = (x-4)/(x+4)
        print rr
        ## print map(rr, range(5))
        for x in range(5):
            print rr(x)

##        p = Polynom((r[1], r[0], r[1]))
##        q = Polynom((r[1], r[0], -r[1]))
##        v = Polynom([r[2], -r[1]])
##        pv = p*v
##        qv = q*v
##        qq = p*v*q*q
##        pp = p*p*v*q
##        
##        d = divmod(pp, qq)
##        print pp == d[0] * qq + d[1]
##        
##        g = gcd(pp, qq)
##        print g
##        print p*v*q
##        print g - p*v*q
##        print g/(p*v*q)