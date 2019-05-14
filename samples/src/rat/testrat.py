## js 27.12.2003


from unittest import makeSuite
from unittest import TestCase
from unittest import TextTestRunner

from rat.rat import *

## globale Variable
r = Rational(2L, 3)         # = 2/3
s = Rational(3, 4)          # = 3/4

class TestRational(TestCase):

    def testCompare(self):
        self.failUnless(r < s)
        self.failUnless(r <= s)
        self.failUnless(not r == s)
        self.failUnless(r != s)
        self.failUnless(not r > s)
        self.failUnless(s == 0.75)
        self.failUnless(0.75 == s)
        self.failUnless(r < 2)
        self.failUnless(r <= 2)
        self.failUnless(not r == 2)
        self.failUnless(not r >= 2)
        self.failUnless(not r > 2)
        self.failUnless(r != 2)
        self.failUnless(not 1 < s)
        self.failUnless(not 1 <= s)
        self.failUnless(not 1 == s)
        self.failUnless(1 >= s)
        self.failUnless(1 > s)
        self.failUnless(1 != s)            
        
    def testPlusMinus(self):
        self.assertEqual(Rational(17, 12), r+s)
        self.assertEqual(Rational(17, 12), s+r)
        self.assertEqual(Rational(5, 3), r+1)
        self.assertEqual(Rational(5, 3), 1+r)
        self.assertEqual(Rational(-1, 3), r-1)
        self.assertEqual(Rational(1, 3), 1-r)
        self.assertEqual(Rational(), s-s)

    def testRat(self):
        self.assertEqual(Rational(r), r)
        self.assertEqual(r/s, Rational(r, s))    

    def testMore(self):
        self.failUnlessEqual(r, abs(r))
        self.failUnlessEqual(0, int(r))
        self.failUnlessEqual(0, long(r))
        self.failUnlessAlmostEqual(0.2/0.3, float(r))

def suite():
    return makeSuite(TestRational)

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())

