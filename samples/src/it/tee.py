## itertools.tee(iterable, n=2)
## Return n independent iterators from a single iterable. Equivalent to:

def tee(iterable, n=2):
    it = iter(iterable)
    deques = [collections.deque() for i in range(n)]

    def gen(mydeque):
        while True:
            if not mydeque:  # when the local deque is empty
                newval = next(it)  # fetch a new value and
                for d in deques:  # load it to all the deques
                    d.append(newval)
            yield mydeque.popleft()

    return tuple(gen(d) for d in deques)
## Once tee() has made a split, the original iterable should not be used anywhere else; 
## otherwise, the iterable could get advanced without the tee objects being informed.

## This itertool may require significant auxiliary storage 
##(depending on how much temporary data needs to be stored). 
## In general, if one iterator uses most or all of the data before another iterator starts, 
## it is faster to use list() instead of tee().
