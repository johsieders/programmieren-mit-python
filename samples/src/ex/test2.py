# test unit 2
# js 29.8.02

import unittest

from ex2 import *


class TestIndex1(unittest.TestCase):
    pass


class TestIndex2(unittest.TestCase):
    pass


class TestAnagram(unittest.TestCase):
    def testAnagram(self):
        xs = ['ttoo', 'nnaa', 'rudi', 'anna', 'duri', 'idur', 'otto']
        ys = ['nnaa', 'anna', 'rudi', 'duri', 'idur', 'ttoo', 'otto']
        xs = anagram_sorted(xs)
        self.assertEqual(ys, xs)


class TestTranslator(unittest.TestCase):
    def m2(x):
        return x % 2 == 0

    def m3(x):
        return x % 3 == 0

    def m5(x):
        return x % 5 == 0

    namespace = {'m2': m2, 'm3': m3, 'm5': m5}

    def testTranslator(self):
        f = translate('m2 m3 AND m5 OR', self.namespace)
        r = [True, False, False, False, False, True, True, False, False, False]
        self.assertEqual(r, [f(n) for n in range(10)])

        f = translate('m2 m3 AND m5 NOT OR', self.namespace)
        r = [True, True, True, True, True, False, True, True, True, True]
        self.assertEqual(r, [f(n) for n in range(10)])


if __name__ == "__main__":
    unittest.main()
