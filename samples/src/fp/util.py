# diverse Utilities
# js 28.2.2002
# verbessert 3.4.04

from functools import reduce


def curry(f, x):  # binds first arg
    return lambda *xs: f(*(x,) + xs)


def rcurry(f, x):  # binds last arg
    return lambda *xs: f(*xs + (x,))


def flip(f):
    return lambda x, y: f(y, x)


def compose(f, g):  # composes f and g
    return lambda *x: f(g(*x))


def binary2nary(f):  # converts s binary function f into an nary one
    return lambda *args: reduce(f, args)


def negate(p):  # negates p
    return lambda x: not p(x)


def unaryAnd(p, q):  # returns p and q
    return lambda x: p(x) and q(x)


def unaryOr(p, q):  # returns p and q
    return lambda x: p(x) or q(x)


def odd(n):
    return n % 2


even = negate(odd)
