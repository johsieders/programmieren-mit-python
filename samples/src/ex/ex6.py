## unit six
## js 5.7.04

from operator import add, mul


def dim(A):  ## returns dimension of A
    return len(A), len(A[0])


def col(A, j):  ## returns j-th column of A
    return [row[j] for row in A]


def vadd(v, w):  ## adds two vectors
    ##  alternativ: vadd = curry(map, add)
    if len(v) != len(w):
        raise ValueError
    return map(add, v, w)


def vmul(v, w):  ## multiplies two vectors
    if len(v) != len(w):
        raise ValueError
    return sum(map(mul, v, w))


def madd(A, B):  ## adds two matrices
    ##  alternativ: madd = curry(map, vadd) = curry(map, curry(map, add))
    if dim(A) != dim(B):
        raise ValueError
    return map(vadd, A, B)


def mmul(A, B):  ## multiplies two matrices
    if dim(A)[1] != dim(B)[0]:
        raise ValueError
    return [[vmul(A[i], col(B, j)) for j in range(len(B[0]))] for i in range(len(A))]


class Matrix(object):
    def __init__(self, rows):
        self.__rows = rows[:]

    def __add__(self, B):
        return madd(self.__rows, B.__rows)

    def __mul__(self, B):
        return mmul(self.__rows, B.__rows)

    def __neg__(self):
        return Matrix([[-self.__rows[i][j] for j in range(len(self.__rows[0]))] for i in range(len(self.__rows))])

    def __sub__(self, B):
        return self + (-B)

    def __repr__(self):
        return repr(self.__rows)
