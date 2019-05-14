## test entwicklungsumgebung
## js 1.4.2010

from tt import intersect
from unittest import *

class MyTestCase(TestCase):
    def test1(self):
        a = (3, 6)
        b = (4, 9)
        c = intersect(a, b)
        self.assertEqual(c, (4, 6))
        f = open('protocol.txt', 'w')
        f.write(str(a) + str(b) + str(c))
        f.flush()
        f.close()


def suite():
    return makeSuite(MyTestCase)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())