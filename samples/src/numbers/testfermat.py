# test fp utilities
# js 2.9.2004

from fp.util import *

from operator import mul
from unittest import makeSuite, TestCase, TestSuite, TextTestRunner
from functools import reduce

def f(x, y, z):
    return x * y * z
    
def g(*xs):
    return reduce(mul, xs)

class TestUtil(TestCase):
    def testCurry(self):
        f1 = curry(f, 2)
        self.assertEqual(24, f1(3, 4))       
        f2 = curry(f1, 3)
        self.assertEqual(24, f2(4))
        f3 = curry(f2, 4)
        self.assertEqual(24, f3())

        g1 = curry(g, 2)
        self.assertEqual(24, g1(3, 4))       
        g2 = curry(g1, 3)
        self.assertEqual(24, g2(4))
        g3 = curry(g2, 4)
        self.assertEqual(24, g3())

    def testRCurry(self):
        f1 = rcurry(f, 2)
        self.assertEqual(24, f1(3, 4))       
        f2 = rcurry(f1, 3)
        self.assertEqual(24, f2(4))
        f3 = rcurry(f2, 4)
        self.assertEqual(24, f3())

        g1 = rcurry(g, 2)
        self.assertEqual(24, g1(3, 4))       
        g2 = rcurry(g1, 3)
        self.assertEqual(24, g2(4))
        g3 = rcurry(g2, 4)
        self.assertEqual(24, g3())
        
def suite():
    suite = TestSuite()    
    suite.addTest(makeSuite(TestUtil))  
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())


