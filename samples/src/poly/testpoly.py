## test polynoms
## js 29.12.03

from unittest import makeSuite, TestCase, TextTestRunner
from poly import *

class TestPolynom(TestCase):
    def testInt(self):
        p = Polynom((1,0,1))
        q = Polynom((1,1))
        self.failUnlessEqual(26, p(5))
        self.failUnlessEqual(101, p(10))
        self.failUnlessEqual(26., p(5.))
        self.failUnlessEqual(101., p(10.))
        self.failUnlessEqual(Polynom((2, 1, 1)), p+q)
        self.failUnlessEqual(Polynom((2, 0, 1)), p+1)
        self.failUnlessEqual(Polynom((2, 0, 1)), 1+p)
        self.failUnlessEqual(Polynom((2, 0, 2)), p*2)
        self.failUnlessEqual(Polynom((2, 0, 2)), 2*p)
        self.failUnlessEqual(Polynom((2, 2, 1)), p(q))
        self.failUnlessEqual(Polynom((2, 0, 1)), q(p))
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), p*q)
        self.failUnlessEqual(Polynom((1, 1, 1, 1)), q*p)

    def testFloat(self):
        p = Polynom((1.,0.,1.))
        q = Polynom((1.,1.))
        self.failUnlessEqual(26., p(5))
        self.failUnlessEqual(101., p(10))
        self.failUnlessEqual(26., p(5.))
        self.failUnlessEqual(101., p(10.))
        self.failUnlessEqual(Polynom((2., 1., 1.)), p+q)
        self.failUnlessEqual(Polynom((2., 0., 1.)), p+1)
        self.failUnlessEqual(Polynom((2., 0., 1.)), 1+p)
        self.failUnlessEqual(Polynom((2., 0., 2.)), p*2)
        self.failUnlessEqual(Polynom((2., 0., 2.)), 2*p)
        self.failUnlessEqual(Polynom((2., 2., 1.)), p(q))
        self.failUnlessEqual(Polynom((2., 0., 1.)), q(p))
        self.failUnlessEqual(Polynom((1., 1., 1., 1.)), p*q)
        self.failUnlessEqual(Polynom((1., 1., 1., 1.)), q*p)

    
def suite():
    return makeSuite(TestPolynom)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
