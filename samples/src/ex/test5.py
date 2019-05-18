## test unit five
## js 29.8.04

import unittest
from ex5 import *


class TestXtuple(unittest.TestCase):

    def testXtuple(self):
        x = xtuple(7)
        r = range(7)
        self.assertEqual(r[0], x[0])
        self.assertEqual(r[6], x[6])
        self.assertEqual(list(r), list(x))
        self.assertEqual(r[2:4], list(x[2:4]))
        self.assertEqual(r[2:], list(x[2:]))
        self.assertEqual(r[:3], list(x[:3]))
        self.assertEqual(r[-1::-1], list(x[-1::-1]))

        x = xtuple(r)
        self.assertEqual(r[0], x[0])
        self.assertEqual(r[6], x[6])
        self.assertEqual(list(r), list(x))
        self.assertEqual(r[2:4], list(x[2:4]))
        self.assertEqual(r[2:], list(x[2:]))
        self.assertEqual(r[:3], list(x[:3]))
        self.assertEqual(r[-1::-1], list(x[-1::-1]))

    def testAdd(self):
        x = xtuple(7) + range(7, 15)
        self.assertEqual(range(15), list(x))
        x = range(7) + xtuple(range(7, 15))
        self.assertEqual(range(15), list(x))
        x = xtuple(7) + xtuple(range(7, 15))
        self.assertEqual(range(15), list(x))

    def testMul(self):
        x = xtuple(7) * 3
        self.assertEqual(3 * list(range(7)), list(x))
        x = 3 * xtuple(7)
        self.assertEqual(3 * list(range(7)), list(x))

    def testMap(self):
        x = xtuple(7)
        y = x.map(lambda n: 2 * n)
        self.assertEqual([2 * n for n in range(7)], list(y))


class TestLazyTuple(unittest.TestCase):
    def testLazyTuple(self):
        x = LazyTuple(70)
        r = range(70)
        self.assertEqual(r[0], x[0])
        self.assertEqual(r[6], x[6])
        self.assertEqual(list(r), list(x))
        self.assertEqual(r[2:4], list(x[2:4]))
        self.assertEqual(r[2:], list(x[2:]))
        self.assertEqual(r[:3], list(x[:3]))
        self.assertEqual(r[-1::-1], list(x[-1::-1]))

    def testAdd(self):
        x = LazyTuple(7) + range(7, 15)
        self.failUnlessEqual(range(15), list(x))

    def testMul(self):
        x = LazyTuple(7) * 3
        self.assertEqual(3 * list(range(7)), list(x))
        x = 3 * LazyTuple(7)
        self.assertEqual(3 * list(range(7)), list(x))

    def testMap(self):
        x = LazyTuple(7)
        y = x.map(lambda n: 2 * n)
        self.assertEqual([2 * n for n in range(7)], list(y))


class TestLazyDictionary(unittest.TestCase):
    def testLazyDictionary(self):
        d = LazyDictionary(range(7))
        self.assertEqual(0, d[0])
        self.assertEqual(None, d.get(7))
        self.assertEqual(range(7), list(d.keys()))
        self.assertEqual(range(7), list(d.values()))
        e = d.copy()
        self.assertEqual(range(7), list(e.keys()))
        self.assertEqual(range(7), list(e.values()))


class TestYdict(unittest.TestCase):
    def testYdict(self):
        d = {0: 0}
        t = ydict(d)
        self.assertEqual(0, t[0])
        self.assertEqual(None, t.get(1))
        self.assertEqual(3, t.get(1, 3))

        t[0] = 5  ## t aendern
        t[1] = 6
        self.assertEqual(5, t[0])
        self.assertEqual(6, t.get(1))
        self.assertEqual(7, t.get(2, 7))

        t.rollback()  ## t zuruecksetzen
        self.assertEqual(0, t[0])
        self.assertEqual(None, t.get(1))
        self.assertEqual(3, t.get(1, 3))

        t[0] = 5  ## t nochmal aendern
        t[1] = 6
        self.assertEqual(5, t[0])
        self.assertEqual(6, t.get(1))
        self.assertEqual(7, t.get(2, 7))

        t.commit()  ## t bestaetigen
        self.assertEqual(5, t[0])
        self.assertEqual(6, t.get(1))
        self.assertEqual(7, t.get(2, 7))

        t.rollback()  ## hat keine Wirkung      
        self.assertEqual(5, t[0])
        self.assertEqual(6, t.get(1))
        self.assertEqual(7, t.get(2, 7))


if __name__ == '__main__':
    unittest.main()
