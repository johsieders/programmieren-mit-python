# js 6.01.02
# Versuche zum Rucksackproblem und zu Branch&Bound

from operator import add, div, mul
from __future__ import nested_scopes

def sortedInd(s):
    t = map(None, s, range(len(s)))
    t.sort(lambda a, b: cmp(b[0], a[0]))
    return map(lambda a: a[1], t)

def knapsack(c, d, D):
    """ max cx s.t. dx <= D, 0 <= xi <= 1 (relaxiertes Problem) """
    sum_c, sum_d = 0, 0
    for i in sortedInd(map(lambda x, y: div(float(x), y), c, d)):
        if sum_d + d[i] <= D:
            sum_c += c[i]
            sum_d += d[i]
        else:
            sum_c += float((D-sum_d))/d[i] * c[i]
            sum_d = D
        if sum_d >= D:
            break
    return sum_c


def restrict(k, c, d, D):
    """ k[i] = 1 (on), 0 (off) or None (free) """
    select = lambda u, v : map(lambda x: x[0], filter(lambda y: y[1] is u, map(None, v, k)))
    cprime = select(None, c)
    dprime = select(None, d)
    cbar   = reduce(add, select(1, c), 0)
    Dprime = D - reduce(add, select(1, d), 0)
    return cbar, cprime, dprime, Dprime


def children(k):
    left, right = k[:], k[:]
    for i in range(len(k)):
        if k[i] is None:
            left[i], right[i] = 1, 0
            return left, right
    return [], []


def leaf(k):
    return len(filter(lambda x: x is None, k)) is 0

def bound(k, c, d, D):
    cbar, cprime, dprime, Dprime = restrict(k, c, d, D)
    val = knapsack(cprime, dprime, Dprime)
    print cbar, cprime, dprime, Dprime, val + cbar, '\n'
    if Dprime >= 0:
        return cbar + val
    else:
        return -1

def val(k, c):
    assert leaf(k)
    return reduce(add, map(mul, k, c))



def search(k, bound, s, c, d, D):
    print k
    
    if bound(k, c, d, D) <= s:
        return 0, []
    
    if leaf(k):  
        v = val(k, c)
        if v > s:
            return v, k     # better solution found
        else:
            return 0, []
        
    left, right = children(k)
    v1, k1 = search(left,  bound, s, c, d, D)
    v2, k2 = search(right, bound, max(s, v1), c, d, D)
    if v1 > v2:
        return v1, k1
    else:
        return v2, k2



c = [9, 8, 10, 4]
d = [50, 50, 60, 50]
D = 100

k0 = [None, None, None, None]
k1 = [1,1,1,1]
k2 = [0,0,0,0]
k3 = [1,0, None, None]

u = [20, 30, 15, 18]
v = [50, 60, 40, 45]
V = 100

r = [7, 3, 4, 9, 6]
s = [21, 18, 12, 18, 24]
t = 90

if __name__ == "__main__":
    # search(k0, bound, 0, c, d, D)
    # search(k0, bound, 40, u, v, V)
    search(5*[None], bound, 25.99, r, s, t)