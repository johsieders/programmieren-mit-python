# test unit four
# js 29.8.02

import unittest
from ex4 import *

class TestInfix(unittest.TestCase):
    def testInfix(self):
        self.assertEqual('x', i2p('x'))
        self.assertEqual('x', i2p('((x))'))
        self.assertEqual('x~', i2p('~x'))
        self.assertEqual('x~ y*', i2p('~x*y'))
        self.assertEqual('x~ y* z+', i2p('~x*y +z'))
        self.assertEqual('x~ y a b+**', i2p('~x*y * (a+b)'))
        self.assertEqual('x~ y a b+**', i2p('~x*y * ((((a)+b)))'))


if __name__ == '__main__':
    unittest.main()