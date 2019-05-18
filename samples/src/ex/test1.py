# test unit one
# js 29.8.02


import unittest

from ex1 import *


class TestUnitOne(unittest.TestCase):
    def testFibo(self):
        self.assertEqual([0, 1, 1, 2, 3, 5, 8, 13, 21, 34], [fibo(n) for n in range(10)])

    def testHistogram(self):
        xs = 100 * [1]
        h = histogram(xs)
        self.assertEqual(list(h.items()), [(1, 100)])

        h = histogram1(xs)
        self.assertEqual(list(h.items()), [(1, 100)])

        h = histogram2(xs)
        self.assertEqual(list(h.items()), [(1, 100)])

        h = histogram3(xs)
        self.assertEqual(list(h.items()), [(1, 100)])

        xs = list(range(100)) * 3
        h = histogram(xs)
        self.assertEqual(h[0], 3)
        self.assertEqual(h[99], 3)

        h = histogram1(xs)
        self.assertEqual(h[0], 3)
        self.assertEqual(h[99], 3)

        h = histogram2(xs)
        self.assertEqual(h[0], 3)
        self.assertEqual(h[99], 3)

        h = histogram3(xs)
        self.assertEqual(h[0], 3)
        self.assertEqual(h[99], 3)

    def testGcd(self):
        self.assertEqual(0, gcd(0, 0))
        self.assertEqual(5, gcd(5, 0))
        self.assertEqual(8, gcd(0, 8))
        self.assertEqual(100, gcd(100, 100))
        self.assertEqual(1, gcd(99, 100))
        self.assertEqual(17, gcd(17 * 23, 17 * 24))

    def testMerge(self):
        self.s = [14, 23, 34, 46]
        self.t = [12, 14, 14, 33, 34, 35]
        self.assertEqual([12, 14, 14, 14, 23, 33, 34, 34, 35, 46], merge(self.s, self.t))

    def testMSort(self):
        self.s = []
        self.assertEqual([], msort(self.s))
        self.s = [7]
        self.assertEqual([7], msort(self.s))
        self.s = [7, 7]
        self.assertEqual([7, 7], msort(self.s))
        self.s = [9, 9, 7, 7, 8, 8]
        self.assertEqual([7, 7, 8, 8, 9, 9], msort(self.s))
        self.s = [15, 2, 4, 7, 23, 0]
        self.assertEqual([0, 2, 4, 7, 15, 23], msort(self.s))

    def testQSort(self):
        self.s = []
        self.assertEqual([], qsort(self.s))
        self.s = [7]
        self.assertEqual([7], qsort(self.s))
        self.s = [7, 7]
        self.assertEqual([7, 7], qsort(self.s))
        self.s = [9, 9, 7, 7, 8, 8]
        self.assertEqual([7, 7, 8, 8, 9, 9], qsort(self.s))
        self.s = [15, 2, 4, 7, 23, 0]
        self.assertEqual([0, 2, 4, 7, 15, 23], qsort(self.s))

    def testNormstring(self):
        self.s = 'aBc uVw'
        self.assertEqual('abcuvw', normstring(self.s))

    def testPalindrome(self):
        b = isPalindrome("")
        self.assertTrue(b)
        b = isPalindrome("x")
        self.assertTrue(b)
        b = isPalindrome("xx")
        self.assertTrue(b)
        b = isPalindrome("xy")
        self.assertFalse(b)

        s = "Reittier"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Reliefpfeiler"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Ein Neger mit Gazelle zagt im Regen nie"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Madam, I'm Adam"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Risotto, Sir?"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Eine treue Familie bei Lima feuerte nie"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Liese, tu Gutes, eil!"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "O Genie, der Herr ehre dein Ego!"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Grub Nero nie in Orenburg?"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Plaudere, du Alp!"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Im Latz Talmi."
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Dogma: I am God."
        b = isPalindrome(s)
        self.assertTrue(b)

    def testZeugnis1(self):
        self.proben = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.kurzproben = [1.0, 1.0, 1.0, 1.0]
        self.stegreifaufgaben = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.resultat = zeugnisnote(self.proben, self.kurzproben, self.stegreifaufgaben)
        self.assertEqual(1.0, self.resultat)

    def testZeugnis2(self):
        self.proben = [2.0, 3.0, 3.0, 2.0, 1.3]
        self.kurzproben = [3.3, 2.7, 4.3, 2.3]
        self.stegreifaufgaben = [4.0, 2.0, 2.3, 5.0, 2.0, 2.3]
        self.resultat = zeugnisnote(self.proben, self.kurzproben, self.stegreifaufgaben)
        self.assertAlmostEqual(2.644827586, self.resultat)


if __name__ == "__main__":
    unittest.main()
