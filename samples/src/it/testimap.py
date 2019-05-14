## Author: Johannes Siedersleben, Munich, Germany.
## siedersleben@sdm.de
## 06-15-2004


#########################################################
## imap (implemented) is different from imap (specified)
#########################################################

from itertools import imap, repeat
from operator import add

# Python implementation of imap
def jmap(function, *iterables):
    iterables = map(iter, iterables)
    while True:
        args = [i.next() for i in iterables]
        if function is None:
            yield tuple(args)
        else:
            yield function(*args)

class c8:
    def next(self):
        return 8
    def __iter__(self):
        print 'start c8'
        return self


## imap and jmap differ
ix = imap(add, repeat(3), c8())     ## start c8
jx = jmap(add, repeat(3), c8())     ## silent


#########################################################
## workaround: delay imap
#########################################################

def delay(it):
    it = iter(it)
    while True:
        yield it.next()


def kmap(function, *iterables):
    return delay(lambda f=function, its=iterables: imap(f, *its))

## imap and jmap differ on c8
kx = kmap(add, repeat(3), c8())     ## silent