## test polynoms
## js 29.12.03

import unittest

from poly import *


class TestPolynom(unittest.TestCase):
    def testInt(self):
        p = Polynom((1, 0, 1))
        q = Polynom((1, 1))
        self.assertEqual(26, p(5))
        self.assertEqual(101, p(10))
        self.assertEqual(26., p(5.))
        self.assertEqual(101., p(10.))
        self.assertEqual(Polynom((2, 1, 1)), p + q)
        self.assertEqual(Polynom((2, 0, 1)), p + 1)
        self.assertEqual(Polynom((2, 0, 1)), 1 + p)
        self.assertEqual(Polynom((2, 0, 2)), p * 2)
        self.assertEqual(Polynom((2, 0, 2)), 2 * p)
        self.assertEqual(Polynom((2, 2, 1)), p(q))
        self.assertEqual(Polynom((2, 0, 1)), q(p))
        self.assertEqual(Polynom((1, 1, 1, 1)), p * q)
        self.assertEqual(Polynom((1, 1, 1, 1)), q * p)

    def testFloat(self):
        p = Polynom((1., 0., 1.))
        q = Polynom((1., 1.))
        self.assertEqual(26., p(5))
        self.assertEqual(101., p(10))
        self.assertEqual(26., p(5.))
        self.assertEqual(101., p(10.))
        self.assertEqual(Polynom((2., 1., 1.)), p + q)
        self.assertEqual(Polynom((2., 0., 1.)), p + 1)
        self.assertEqual(Polynom((2., 0., 1.)), 1 + p)
        self.assertEqual(Polynom((2., 0., 2.)), p * 2)
        self.assertEqual(Polynom((2., 0., 2.)), 2 * p)
        self.assertEqual(Polynom((2., 2., 1.)), p(q))
        self.assertEqual(Polynom((2., 0., 1.)), q(p))
        self.assertEqual(Polynom((1., 1., 1., 1.)), p * q)
        self.assertEqual(Polynom((1., 1., 1., 1.)), q * p)


if __name__ == '__main__':
    unittest.main()
