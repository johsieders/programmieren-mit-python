## js 1.9.2004
## iterator utilities
## reworked 1/9/2011

from itertools import  cycle, islice, izip
from operator import add


def removeDups(t):
    t = iter(t)
    last = next(t)
    yield last
    
    while True:
        x = next(t)
        if x != last:
            last = x
            yield last
    

def weak(op):
    """ op: a binary operator
        weak(op): a binary operator accepting one or two Nones
    """
    def aux(x, y):
        if x is None:
            return y
        elif y is None:
            return x
        else:
            return op(x, y)
    return aux

wadd = weak(add)


def take(n, j):
    """ yields the first n elements of iterator j """
    return tuple(islice(j, n))


def fun(f, *args): 
    """ assume two args: arg0, arg1.
        Then fun yields:
        arg0, arg1, f(arg0, arg1), f(arg1, f(arg0, arg1)), ..
    """

    for arg in args:
        yield arg
    while True: 
        args = args[1:] + (f(*args),)
        yield args[-1]

ari  = lambda increment : fun(lambda x : x + increment, 0)
geo  = lambda factor : fun(lambda x : x * factor, 1)
fibo = lambda : fun(add, 1, 1)


def faculty():
    """ the faculty sequence"""
    factor = 1
    current = 1
    while True:
        yield current
        current *= factor
        factor += 1

        
exp = lambda : (1.0/k for k in faculty())
cos = lambda : (a * b for a, b in izip(cycle((1, 0, -1, 0)), exp()))
sin = lambda : (a * b for a, b in izip(cycle((0, 1, 0, -1)), exp()))

avg = lambda xs : (1.0 * sum(xs))/len(xs)
