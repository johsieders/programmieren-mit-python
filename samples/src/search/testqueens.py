## compare different implementations of queens
## js 10.8.02

import unittest
from time import time

from test.test_generators import Queens

from queens import *


class TestQueens(unittest.TestCase):
    def test(self):
        n = 4
        t = []

        print("\nstart queens")

        ##        t.append(time())
        ##        s = SearchByClass(QueensProblem(n))
        ##        print len(s.search())

        t.append(time())
        print
        len(list(searchByFunction(QueensProblem(n))))

        t.append(time())
        print
        len(list(searchByGenerator(QueensProblem(n))))

        t.append(time())
        print
        len(list(queens_conjoin(n)))

        t.append(time())
        q = Queens(n)
        print
        len(list(q.solve()))

        t.append(time())

        qq = ['SearchByClass', 'searchByFunction', 'searchByGenerator', 'queen_conjoin', 'Queens']

        for q, t in zip(qq, [t[i + 1] - t[i] for i in range(len(qq))]):
            print
            q, t

        print
        "stop queens"


def suite():
    return unittest.makeSuite(TestQueens)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
