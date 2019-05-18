# Ein Simplex-Versuch mit NumPy
# js
# 29.12.01

from LinearAlgebra import *
from Numeric import *


class Simplex:
    def __init__(self, A, b, c):
        self.m, self.n = A.shape
        assert self.m is b.shape[0], 'b has wrong dimension'
        assert self.n is c.shape[0], 'c has wrong dimension'
        self.A = A
        self.b = b
        self.c = c

    def setBase(self, baseIndices):
        assert len(baseIndices) is self.m, 'wrong number of base indices'
        self.baseIndices = baseIndices
        self.cB = take(self.c, baseIndices)
        self.Binv = inverse(take(self.A, baseIndices, 1))
        self.xB = dot(self.Binv, self.b)
        self.value = dot(self.cB, self.xB)
        print
        self

    def tryNBIndex(self, q):
        return self.c[q] - dot(self.cB, (dot(self.Binv, self.A[:, q])))

    def pivot(self, q):
        y = dot(self.Binv, self.A[:, q])
        minval = 1000000
        p = -1
        for k in range(self.m):
            if y[k] > 0 and self.xB[k] / y[k] < minval:
                minval = y[k]
                p = self.baseIndices[k]
        if p < 0:  # problem unbounded
            return -1

        self.baseIndices.remove(p)
        self.baseIndices.append(q)
        self.setBase(self.baseIndices)
        return 0

    def solve(self):
        q = 0
        while q < self.n:
            if q not in self.baseIndices and self.tryNBIndex(q) > 0:
                break
            else:
                q += 1

        if q is self.n:
            return 0  # optimal solution

        rc = self.pivot(q)
        if rc < 0:
            return rc  # problem unbounded

        return self.solve()  # once again

    def __str__(self):
        return 'Base Indices:  ' + `self.baseIndices` + '\n' + \
               'Base Inverse:  ' + `self.Binv` + '\n' + \
               'Base Solution: ' + `self.xB` + '\n' + \
               'Value: ' + `self.value` + '\n'


A1 = array([[2, 1, 1, 1], [1, -1, 2, 1]])
b1 = array((10, 2))
c1 = array((10, 4, 8, 6))

A2 = array([[1, -1, 1, 1], [-1, 1, 2, 2]])
b2 = array((8, 19))
c2 = array((2, 4, 7, 6))

A3 = array([[2, -5, -2], [1, -1, 0]])
b3 = array((3, 2))
c3 = array((3, -6, -1))

A4 = array([[1, 2, -1, 0, 0, 0],
            [2, -1, -1, 1, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [1, 2, -2, 0, 0, -2]])
b4 = array([6, 14, 11, 2])
c4 = array([1, -1, 1, 0, 0, 0])

A5 = array([[2, 3, 2],
            [4, -4, -1]])
b5 = array([6, 8])
c5 = array([2, 7, 1])

A6 = array([[-7, 1, 3, -1],
            [-2, 1, 1, -1]])
b6 = array([0, 0])
c6 = array([1, 3, 4, 0])


def test():
    s = Simplex(A1, b1, c1)
    s.setBase([0, 1])
    print
    s.solve()

    s = Simplex(A2, b2, c2)
    s.setBase([1, 2])
    print
    s.solve()

    s = Simplex(A3, b3, c3)
    s.setBase([0, 1])
    print
    s.solve()

    s = Simplex(A5, b5, c5)
    s.setBase([0, 2])
    print
    s.solve()

    # s = Simplex(A4, b4, c4)
    # s.setBase([0,1])
    # print s.solve()


if __name__ == '__main__':
    test()
