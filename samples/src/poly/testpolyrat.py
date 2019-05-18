## test polynoms
## js 29.12.03

from unittest import makeSuite, TestCase, TextTestRunner

from poly import *
from rat import *


class TestPolynom(TestCase):
    def testInt(self):
        p = Polynom((1, 0, 1))
        q = Polynom((1, 1))
        self.failUnlessEqual(26, p(5))
        self.failUnlessEqual(101, p(10))
        self.failUnlessEqual(26., p(5.))
        self.failUnlessEqual(101., p(10.))
        self.failUnlessEqual(Polynom((2, 1, 1)), p + q)
        self.failUnlessEqual(Polynom((2, 0, 1)), p + 1)
        self.failUnlessEqual(Polynom((2, 0, 1)), 1 + p)
        self.failUnlessEqual(Polynom((2, 0, 2)), p * 2)
        self.failUnlessEqual(Polynom((2, 0, 2)), 2 * p)
        self.failUnlessEqual(Polynom((2, 2, 1)), p(q))
        self.failUnlessEqual(Polynom((2, 0, 1)), q(p))
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), p * q)
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), q * p)

    def testFloat(self):
        p = Polynom((1., 0., 1.))
        q = Polynom((1., 1.))
        self.failUnlessEqual(26., p(5))
        self.failUnlessEqual(101., p(10))
        self.failUnlessEqual(26., p(5.))
        self.failUnlessEqual(101., p(10.))
        self.failUnlessEqual(Polynom((2., 1., 1.)), p + q)
        self.failUnlessEqual(Polynom((2., 0., 1.)), p + 1)
        self.failUnlessEqual(Polynom((2., 0., 1.)), 1 + p)
        self.failUnlessEqual(Polynom((2., 0., 2.)), p * 2)
        self.failUnlessEqual(Polynom((2., 0., 2.)), 2 * p)
        self.failUnlessEqual(Polynom((2., 2., 1.)), p(q))
        self.failUnlessEqual(Polynom((2., 0., 1.)), q(p))
        self.failUnlessEqual(Polynom((1., 1., 1., 1.)), p * q)
        self.failUnlessEqual(Polynom((1., 1., 1., 1.)), q * p)

    def testRat(self):
        pass
        zero = Rational(0, 1)
        one = Rational(1, 1)
        two = Rational(2, 1)

        p = Polynom((one, zero, one))
        q = Polynom((one, one))

        self.failUnlessEqual(Polynom((two, one, one)), p + q)
        self.failUnlessEqual(Polynom((two, zero, one)), p + 1)
        self.failUnlessEqual(Polynom((two, zero, one)), 1 + p)
        self.failUnlessEqual(Polynom((two, zero, two)), p * 2)
        self.failUnlessEqual(Polynom((2, 0, 2)), 2 * p)

        self.failUnlessEqual(Polynom((2, 0, 1)), p + one)
        self.failUnlessEqual(Polynom((2, 0, 2)), p * two)
        ####      doesn't work because p is coerced to Rational
        ##        self.failUnlessEqual(Polynom((two, zero, one)), one+p)
        ##        self.failUnlessEqual(Polynom((two, zero, two)), two*p)
        self.failUnlessEqual(Polynom((2, 2, 1)), p(q))
        self.failUnlessEqual(Polynom((2, 0, 1)), q(p))
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), p * q)
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), q * p)

    def testDivision(self):
        pass
        p = Polynom((2, 0, 1))
        q = Polynom((1, -1))
        d = divmod(p, q)
        self.failUnlessEqual(p, d[0] * q + d[1])

        p = Polynom([0])
        q = Polynom([1])
        d = divmod(p, q)
        self.failUnlessEqual(p, d[0] * q + d[1])

        p = Polynom([1.])
        q = Polynom([2.])
        d = divmod(p, q)
        self.failUnlessEqual(p, d[0] * q + d[1])

        p = Polynom((2., 3., 4., 5.))
        q = Polynom((3., 4.))
        d = divmod(p, q)
        self.failUnlessEqual(p, d[0] * q + d[1])

        d = divmod(p * q, q)
        self.failUnlessEqual(p * q, d[0] * q + d[1])
        d = divmod(p * q, p)
        self.failUnlessEqual(p * q, d[0] * p + d[1])

    def testGcd(self):
        pass
        p = Polynom((-1, 0, 1))  ## x**2 - 1
        q = Polynom((-1, 1))  ## x - 1
        g = gcd(p, q)  ## g = x-1
        self.failUnless(not p % g)
        self.failUnless(not q % g)

        r = map(Rational, range(20), 20 * [1])  ## 0/1, 1/1, 2/1, ..

        p = Polynom((-r[1], r[0], r[1]))  ## (x - 1)(x + 1)
        q = Polynom((-r[1], r[1]))  ## x - 1
        g = gcd(p, q)
        self.failUnless(not p % g)
        self.failUnless(not q % g)

        u = p * q
        self.failUnless(gcd(u, q) == q)
        self.failUnless(gcd(u, p) == p)

        v = Polynom([r[2]])
        pv = p * v
        qv = q * v
        d = divmod(pv, qv)
        self.failUnless(pv == d[0] * qv + d[1])
        self.failUnless(gcd(pv, qv) == qv)

        p = Polynom((r[1], r[0], r[1]))
        q = Polynom((r[1], r[0], -r[1]))
        v = Polynom([r[2], -r[1]])
        pv = p * v
        qv = q * v
        d = divmod(pv, qv)
        g = gcd(pv, qv)  ## g == (4, -2)!!
        self.failUnless(pv == d[0] * qv + d[1])
        self.failUnless(gcd(pv, qv) == 2 * v)
        self.failUnless(not pv % g)
        self.failUnless(not qv % g)

        qq = p * v * q * q
        pp = p * p * v * q
        d = divmod(pp, qq)
        self.failUnless(pp == d[0] * qq + d[1])
        g = gcd(pp, qq)
        self.failUnless(g == 2 * p * v * q)
        self.failUnless(not pp % g)
        self.failUnless(not qq % g)

        p = Polynom((-3., 2., 8., 9.))
        q = Polynom((-3., 10.))
        g = gcd(p * q, q)
        self.failUnlessEqual(g, q)
        g = gcd(p * q, p)
        self.failUnlessEqual(g, p)

    ##        u = Polynom((7., 3., 6.))
    ##        g = gcd(p*u, q*u)   ## todo
    ##        self.failUnlessEqual(g, u)

    def testRatPoly(self):
        r = map(Rational, range(2), 2 * [1])

        p = Polynom((-r[1], r[0], r[1]))  ## (x - 1)(x + 1)
        q = Polynom((-r[1], r[1]))  ## x - 1
        rr = Rational(p, q)
        self.failUnlessEqual(rr, Polynom((r[1], r[1])))

    def testDivRat(self):
        pass
        zero = Rational(0, 1)
        one = Rational(1, 1)
        two = Rational(2, 1)

        p = Polynom((one, zero, one))
        q = Polynom((one, one))

        d = divmod(p, q)
        self.failUnlessEqual(p, d[0] * q + d[1])
        d = divmod(q, p)
        self.failUnlessEqual(q, d[0] * p + d[1])

    def testMore(self):
        p = [Polynom([0] * n + [1]) for n in range(10)]
        self.failUnlessEqual(Polynom([1] * 10), sum(p))
        r = reduce(lambda a, b: a + 2 * b, p)
        r = reduce(lambda a, b: a * b, p)
        r = p[8] * p[9] + p[3]
        self.assertEqual(divmod(r, p[8]), (p[9], p[3]))
        self.assertEqual(divmod(r, p[9]), (p[8], p[3]))


def suite():
    return makeSuite(TestPolynom)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
