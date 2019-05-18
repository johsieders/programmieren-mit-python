## beispiele mit numpy

import numpy as np

a = np.arange(4)
b = np.arange(12)
c = np.arange(24)

a.shape = (4)
b.shape = (3, 4)
c.shape = (2, 3, 4)


def expand(a, b):
    """ a und b sind zwei arrays.
        1) wenn a.shape == b.shape, dann ist nichts zu tun
        2) wenn a.rank < b.rank, dann vertausche a und b
        3) Jetzt ist a.rank >= b.rank
        4) repliziere b an den Achsen wo gilt
           a.shape[i] > b.shape[i] und b.shape=1 """

    if a.shape == b.shape:
        return a, b  # nichts zu tun

    if a.rank < b.rank:
        a, b = b, a  # jetzt ist a.rank >= b.rank

    b.shape = (1,) * (a.rank - b.rank) + b.shape
    # jetzt ist a.rank == b.rank

    if np.alltrue(np.less_equal(a.shape, b.shape)):
        a, b = b, a  # jetzt ist a.shape >= b.shape
    elif np.alltrue(np.less_equal(b.shape, a.shape)):
        pass
    else:
        raise 'a nicht kompatibel mit b'

    for i in range(a.rank):
        if a.shape[i] == b.shape[i]:
            pass
        elif b.shape[i] == 1:
            b = np.repeat(b, a.shape[i], i)
        else:
            raise 'a nicht kompatibel mit b'
    return a, b
