# Python Test Intervalle
# js, 8.6.04

from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from vlist import *

N = 100


class TestInterval(TestCase):

    def testMake(self):
        v = Vlist((None, None), )
        self.failUnlessEqual('()[]', str(v))

    def testContains(self):
        v = Vlist((None, True), )
        self.failUnless(-1 in v)
        self.failUnless(0 in v)
        self.failUnless(1 in v)

        v = Vlist((None, False), (0, True), (10, False))
        self.failUnless(0 in v)
        self.failUnless(9.9 in v)
        self.failUnless(10 not in v)

    def testIntersection(self):
        v = Vlist((None, True), (0, False))
        v = Vlist((None, False), (0, True))
        self.failUnlessEqual(iv.emptyInterval, v & w)

        v = Vlist((None, False), (0, True), (10, False))
        self.failUnlessEqual(v, v & v)
        self.failUnlessEqual(+v, v & +v)
        w = Vlist((None, False), (0, True), (12, False))
        self.failUnlessEqual(v, v & w)
        self.failUnlessEqual(+v, v & +w)
        w = Vlist((None, False), (3, True), (12, False))
        z = Vlist((None, False), (3, True), (10, False))
        self.failUnlessEqual(z, v & w)
        self.failUnlessEqual(+z, v & +w)

    def testUnion(self):
        v = Vlist((None, False), (0, True), (1, False))
        w = Vlist((None, False), (0, True), (1, False))
        self.failUnlessEqual(+w, v | w)

    def testDifference(self):
        v = Vlist((None, False), (0, True), (4, False))
        w = Vlist((None, False), (2, True), (6, False))
        r = Vlist((None, False), (0, True), (2, False))
        s = Vlist((None, False), (4, True), (6, False))

        self.failUnlessEqual(r, v - w)
        self.failUnlessEqual(s, w - v)
        self.failUnlessEqual(v ^ w, (v - w) | (w - v))
        self.failUnlessEqual(v ^ w, (v | w) - (v & w))

    def testEmpty(self):
        e = Vlist((None, False), )
        self.failUnlessEqual(e, e)
        self.failUnless(not e < e)

    def testHard(self):
        vs = Vlist(((None, False),) + zip(((a, a + 10) for a in range(N)), cycle(True, False)))

        self.failUnlessEqual(+iv(-oo, oo), vs | -vs)
        self.failUnlessEqual(+iv(), vs & -vs)

    def testHarder(self):
        vs = Intervals([iv(a, a + 1, False, False) for a in range(N)], True)
        self.failUnlessEqual(+iv(-oo, oo), vs | -vs)
        self.failUnlessEqual(+iv(), vs & -vs)

    def testClosure(self):
        vs = Intervals([iv(a, a + 1, False, False) for a in range(N)], True)
        self.failUnlessEqual(+iv(0, N, True, True), vs.closure())


def suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterval))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
