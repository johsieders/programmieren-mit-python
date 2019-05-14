# Python Test Intervalle
# js, 8.6.04
# js 25.12.04

from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from vlist import *

N = 100000

class TestInterval(TestCase):
    def testIntersection(self):
        v = iv((0, 10), (20, 30))
        w = v.intersect((-10, -5))
        self.failUnlessEqual(w, iv())

        w = v.intersect((-10, 0))
        self.failUnlessEqual(w, iv())

        w = v.intersect((-10, 5))
        self.failUnlessEqual(w, iv((0, 5)))

        w = v.intersect((-10, 10))
        self.failUnlessEqual(w, iv((0, 10)))

        w = v.intersect((-10, 15))
        self.failUnlessEqual(w, iv((0, 10)))

        w = v.intersect((-10, 20))
        self.failUnlessEqual(w, iv((0, 10)))

        w = v.intersect((-10, 25))
        self.failUnlessEqual(w, iv((0, 10), (20, 25)))

        w = v.intersect((-10, 30))
        self.failUnlessEqual(w, iv((0, 10), (20, 30)))

        w = v.intersect((-10, 35))
        self.failUnlessEqual(w, iv((0, 10), (20, 30)))

        ## untere Grenze wandert, obere Grenze fest
        w = v.intersect((35, 40))
        self.failUnlessEqual(w, iv())

        w = v.intersect((30, 40))
        self.failUnlessEqual(w, iv())

        w = v.intersect((25, 40))
        self.failUnlessEqual(w, iv((25, 30)))

        w = v.intersect((20, 40))
        self.failUnlessEqual(w, iv((20, 30)))

        w = v.intersect((15, 40))
        self.failUnlessEqual(w, iv((20, 30)))

        w = v.intersect((10, 40))
        self.failUnlessEqual(w, iv((20, 30)))

        w = v.intersect((5, 40))
        self.failUnlessEqual(w, iv((5, 10), (20, 30)))

        w = v.intersect((0, 40))
        self.failUnlessEqual(w, iv((0, 10), (20, 30)))

        w = v.intersect((-10, 40))
        self.failUnlessEqual(w, iv((0, 10), (20, 30)))


    def testAppend(self):
        v = iv((0, 10), (20, 30))
        v.append((-10, -5))
        self.failUnlessEqual(v, iv((-10, -5), (0, 10), (20, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 0))
        self.failUnlessEqual(v, iv((-10, 10), (20, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 5))
        self.failUnlessEqual(v, iv((-10, 10), (20, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 10))
        self.failUnlessEqual(v, iv((-10, 10), (20, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 15))
        self.failUnlessEqual(v, iv((-10, 15), (20, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 20))
        self.failUnlessEqual(v, iv((-10, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 25))
        self.failUnlessEqual(v, iv((-10, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 30))
        self.failUnlessEqual(v, iv((-10, 30)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 35))
        self.failUnlessEqual(v, iv((-10, 35)))

        ## untere Grenze wandert, obere Grenze fest
        v = iv((0, 10), (20, 30))
        v.append((35, 40))
        self.failUnlessEqual(v, iv((0, 10), (20, 30), (35, 40)))

        v = iv((0, 10), (20, 30))
        v.append((30, 40))
        self.failUnlessEqual(v, iv((0, 10), (20, 40)))

        v = iv((0, 10), (20, 30))
        v.append((25, 40))
        self.failUnlessEqual(v, iv((0, 10), (20, 40)))

        v = iv((0, 10), (20, 30))
        v.append((20, 40))
        self.failUnlessEqual(v, iv((0, 10), (20, 40)))

        v = iv((0, 10), (20, 30))
        v.append((15, 40))
        self.failUnlessEqual(v, iv((0, 10), (15, 40)))

        v = iv((0, 10), (20, 30))
        v.append((10, 40))
        self.failUnlessEqual(v, iv((0, 40)))

        v = iv((0, 10), (20, 30))
        v.append((5, 40))
        self.failUnlessEqual(v, iv((0, 40)))

        v = iv((0, 10), (20, 30))
        v.append((0, 40))
        self.failUnlessEqual(v, iv((0, 40)))

        v = iv((0, 10), (20, 30))
        v.append((-10, 40))
        self.failUnlessEqual(v, iv((-10, 40)))


    def testMake(self):
        vs = iv()


    def testContains(self):
        v = iv((None, None))
        self.failUnless(-1 in v)
        self.failUnless(0 in v)
        self.failUnless(1 in v)

        v = iv((0, 10))
        self.failUnless(0 in v)
        self.failUnless(9.9 in v)
        self.failUnless(10 not in v)

    def testAnd(self):
        v = iv((None, 0))
        w = iv((0, None))
        self.failUnlessEqual(iv(), v & w)

        v = iv((0, 10))
        self.failUnlessEqual(v, v & v)
        self.failUnlessEqual(+v, v & +v)

        w = iv((0, 20))
        self.failUnlessEqual(v, v & w)
        self.failUnlessEqual(+v, v & +w)

        w = iv((5, 15))
        self.failUnlessEqual(iv((5, 10)), v & w)
        self.failUnlessEqual(+iv((5, 10)), v & +w)


    def testUnion(self):
        v = iv((0, 1))
        w = iv((0, 1))
        self.failUnlessEqual(w, v | w)
        self.failUnlessEqual(w, w | v)

        w = v | iv((1, 2))
        self.failUnlessEqual(w, iv((0, 2)))

        w = v | iv((2, 3))
        self.failUnlessEqual(w, iv((0, 1), (2, 3)))


    def testDifference(self):
        pass
        v = iv((0, 4))
        w = iv((2, 6))
        self.failUnlessEqual(v - w, iv((0, 2)))
        self.failUnlessEqual(w - v, iv((4, 6)))
        self.failUnlessEqual(v ^ w, (v - w) | (w - v))
        self.failUnlessEqual(v ^ w, (v | w) - (v & w))


    def testEmpty(self):
        e = iv()
        self.failUnlessEqual(e, e)
        self.failUnless(not e < e)
        self.failUnlessEqual('', repr(e))
        self.failIf(-1 in e)
        self.failIf(0 in e)
        self.failIf(1 in e)


    def testHard(self):
        vs = iv(*[(a, a + 10) for a in range(0, 1000, 20)])
        self.failUnlessEqual(500, vs.sum())
        self.failUnlessEqual(iv((None, None)), vs | -vs)
        self.failUnlessEqual(iv(), vs & -vs)

    def testHarder(self):
        vs = iv(*[(a, a + 1) for a in range(N)])
        self.failUnlessEqual(iv((None, None)), vs | -vs)
        self.failUnlessEqual(iv(), vs & -vs)


def suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterval))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
