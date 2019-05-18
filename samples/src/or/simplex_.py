# ein Versuch, das Simplexverfahren mit Python zu implementieren
# js 28.12.01

from __future__ import nested_scopes

from UserDict import UserDict


class Matrix(UserDict):
    def __init__(self, data, n, m):
        """ data: Verzeichnis der Eintraege, m = Anzahl Zeilen, n = Anzahl Spalten """
        UserDict.__init__(self, data)
        self.n = n
        self.m = m

    def __call__(self, i, j):
        """ liefere Element an der Position i, j """
        assert (0 < i and i <= self.m)
        assert (0 < j and j <= self.n)
        if self.has_key((i, j)):
            return self[(i, j)]
        else:
            return 0

    def row(self, i):
        return map(lambda j: self(i, j), range(1, self.n + 1))

    def column(self, j):
        return map(lambda i: self(i, j), range(1, self.m + 1))

    def rows(self):
        return map(self.row, range(1, self.n + 1))

    def columns(self):
        return map(self.column, range(1, self.m + 1))

    def elementaryOperation(self, i, j, a):
        for h in range(1, self.n + 1):
            self[(j, h)] = self(j, h) + a * self(i, h)
            if not self[(j, h)]:
                del self[(j, h)]

    def inv(self, p=1):
        assert (self.n is self.m)
        if p is self.n:
            return
        # c = Menge der Zeilenindizes mit self[i, p] != 0
        c = filter(lambda i: self(i, p), range(p, self.m + 1))
        assert (c, 'Matrix singulaer')
        i = c[0]
        for j in c[1:]:
            self.elementaryOperation(i, j, -1.0 * self(j, p) / self(i, p))
        self.inv(p + 1)


d = {(1, 1): 17, (1, 2): 12, (1, 3): 13, \
     (2, 1): 21, (2, 2): 22, (2, 3): 23, \
     (3, 1): 31, (3, 2): 32, (3, 3): 33}

e = {(1, 1): 1, (1, 2): 2, (1, 3): 2, \
     (2, 1): 2, (2, 2): 2, (2, 3): 1, \
     (3, 2): 1, (3, 3): 1}

m = Matrix(d, 3, 3)

# m.inv()
