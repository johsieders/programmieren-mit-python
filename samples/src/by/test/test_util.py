import unittest

from by.util.binaries import *


class TestUtil(unittest.TestCase):
    def test_binary_cube(self):
        c = list(binary_cube(()))
        c = list(binary_cube((0,)))
        c = list(binary_cube((None,)))
        c = list(binary_cube((0, 0)))
        c = list(binary_cube((0, None)))
        c = list(binary_cube((None, 0)))
        c = list(binary_cube((None, None)))
        c = list(binary_cube((0, 1, None, 0, 1, None, 0, 1, None)))
        print(c)

    def test_intbin(self):
        def id1(b):
            return int2bin((bin2int(b)), len(b))

        def id2(i):
            return bin2int(int2bin(i, log2(i)))

        for i in range(1000):
            self.assertEqual(i, id2(i))

        for i in range(2 ** 10):
            b = int2bin(i, log2(i))
            self.assertEqual(b, id1(b))

    def test_rev_int(self):
        for i in range(100000):
            rev_int(i, 20)

    def test_bin2int(self):
        for i in range(100000):
            b = int2bin(i, 15)
            bin2int(b)

    def test_bin2int_(self):
        for i in range(100000):
            b = int2bin(i, 15)
            bin2int_(b)

    def test_int2bin(self):
        print()
        for i in range(100000):
            int2bin(i, 20)

    def test_int2bin_(self):
        print()
        for i in range(100000):
            int2bin_(i, 20)


if __name__ == '__main__':
    unittest.main()
