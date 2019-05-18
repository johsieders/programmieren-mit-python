## conjoin as alternative to search
## js 10.8.02
## bubenorbis

from test.test_generators import conjoin

a = [None]
for a[0] in range(3):
    pass


##      would print
##        [0]
##        [1]
##        [2]

# from test_generators
# do not touch
def simple_conjoin(gs):
    def gen(i, state):
        if i == len(gs):
            yield state
        else:
            for state[i] in gs[i]():
                for x in gen(i + 1, state):
                    yield x

    for x in gen(0, [None] * len(gs)):
        yield x


g = lambda: range(2)
cs = simple_conjoin((g, g, g))


##      yields
##        [0, 0, 0]
##        [0, 0, 1]
##        [0, 1, 0]
##        [0, 1, 1]
##        [1, 0, 0]
##        [1, 0, 1]
##        [1, 1, 0]
##        [1, 1, 1]


def permutations(seq):
    gs = []
    state = len(seq) * [None]

    for i in range(len(seq)):
        def g(i=i):
            for x in seq:
                if x not in state[:i]:
                    state[i] = x
                    yield x

        gs.append(g)

    ##  return simple_conjoin(gs)
    ##  return flat_conjoin(gs)
    return conjoin(gs)
