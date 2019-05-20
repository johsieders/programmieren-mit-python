# unit five
# js 10.3.2004


# from types import IntType, LongType, SliceType

flip = lambda f: lambda x, y: f(y, x)  # flips args
compose = lambda f, g: lambda x: f(g(x))  # composes f and g


############################
## list with transactions ##
############################ 

class talist(list):
    def __init__(self, xs=[]):
        list.__init__(self, xs)
        self.before = xs[:]

    def rollback(self):
        self[:] = self.before

    def commit(self):
        self.before[:] = self


#################################
### xtuple: a functional list ###
#################################

class xtuple(tuple):
    """xtuple-elements are computed on demand."""

    def __init__(self, s, compute = lambda n : n):
        """ Entweder:
        a) s ist Laenge, compute berechnet das i-te Element. Oder:
        b) s ist andere Sequenz; compute ist Zugriff auf i-tes Element von s """
        tuple.__init__(self)
        if isinstance(s, int):
            self.compute = compute
            self.length = s
        else:               # s knows [] and len()
            self.compute = lambda n: s[n]
            self.length = len(s)

    def __len__(self):
        return self.length

    def __getitem__(self, s):
        if isinstance(s, int):
            if -len(self) <= s < 0:
                return self[s + len(self)]
            elif s < self.length:
                return self.compute(s)
            else:
                raise IndexError
        elif isinstance(s, slice):
            x = range(*s.indices(len(self)))    # return xtuple
            return xtuple(len(x), lambda i: self[x[i]])

        else:
            raise TypeError

    def __add__(self, other):
        def tmp(n):
            if n < len(self):
                return self[n]
            else:
                return other[n - len(self)]

        return xtuple(len(self) + len(other), tmp)

    def __mul__(self, k):
        if not isinstance(k, int):
            raise TypeError
        return xtuple(k * len(self), lambda n: n % len(self))

    def map(self, f):
        return xtuple(len(self), compose(f, self.compute))

    ##    def __cmp__(self, other):
    ##        for i in range(min(len(self), len(other))):
    ##            a, b = self[i], other[i]
    ##            if a < b:
    ##                return -1
    ##            elif a > b:
    ##                return 1
    ##        return len(self) - len(other)

    __radd__ = flip(__add__)
    __rmul__ = __mul__

    def __repr__(self):
        return 'xtuple(' + repr(len(self)) + ')'


## 2b
class LazyTuple(object):
    """ load(a, b) laedt den Bereich [a:b];
        length: Laenge des Tupels
        loadhead: soviel Elemente werden im Voraus geladen
    """

    def __init__(self, s,
                 load=lambda a, b: range(a, b),
                 loadAhead=10):
        """ Entweder:
        a) s ist Laenge, load(a, b) laedt den Bereich [a:b]. Oder:
        b) s ist andere Sequenz; load laedt Bereich von s """
        if isinstance(s, int):
            self.length = s
            self.load = load
        else:  ## s kann [:] und len()
            self.load = lambda a, b: s[a:b]
            self.length = len(s)

        self.loadAhead = loadAhead
        self.cache = []

    def __len__(self):
        return self.length

    def __getitem__(self, s):
        if isinstance(s, int):
            if -len(self) <= s < 0:
                return self[s + len(self)]
            elif len(self.cache) <= s < len(self):  ## nachladen
                self.cache += self.load(len(self.cache), min(s + self.loadAhead, len(self)))
            return self.cache[s]
        elif isinstance(s, slice):
            x = range(*s.indices(len(self)))
            return LazyTuple(xtuple(len(x), lambda i: self[x[i]]))
        else:
            raise TypeError

    def __add__(self, other):
        return LazyTuple(xtuple(self) + xtuple(other))

    def __mul__(self, n):
        return LazyTuple(xtuple(self) * n)

    def map(self, f):
        return LazyTuple(xtuple(len(self), lambda i: f(self[i])))

    def __cmp__(self, other):
        for i in range(min(len(self), len(other))):
            a, b = self[i], other[i]
            if a < b:
                return -1
            elif a > b:
                return 1
        return len(self) - len(other)

    def __repr__(self):
        return 'LazyTuple(' + repr(len(self)) + ')'

    __radd__ = flip(__add__)
    __rmul__ = __mul__


# 2c
class LazyDictionary(object):
    def __init__(self, keys, load=lambda x: x):
        """ keys = list of all keys, load(key) loads value """
        self.keyList = list(keys)
        self.cache = {}
        self.load = load

    def __len__(self):
        return len(self.keyList)

    def __getitem__(self, key):
        if key not in self.keys():
            raise KeyError
        if key not in self.cache.keys():
            self.cache[key] = self.load(key)
        return self.cache[key]

    def keys(self):
        return list(self.keys())

    def values(self):
        return xtuple(len(self), lambda n: self.load(self.keys()[n]))

    def items(self):
        return xtuple(len(self), lambda n: self.keys()[n], self.load(self.keys()[n]))

    def has_key(self, key):
        return key in self.keys()

    def get(self, key, default=None):
        if key not in self.keys():
            return default
        if key not in self.cache.keys():
            self.cache[key] = self.load(key)
        return self.cache[key]

    def copy(self):
        return LazyDictionary(self.keyList, self.load)

    def __repr__(self):
        return repr(self.items())

    ## 2d


class xdict(dict):
    def __init__(self, load, store, delete):
        """ load(key) : load value
            store(key, value): speichere value unter key
            delete(key): loescht den Eintrag unter key"""
        dict.__init__(self)
        self.deleted = []
        self.load = load
        self.store = store
        self.delete = delete

    def get(self, key, default=None):
        value = dict.get(self, key, default)
        if value is default:
            try:
                value = self.load(key)
            except KeyError:
                pass  ## value = default
        return value

    def __delitem__(self, key):
        dict.__delitem__(key)
        self.deleted.append(key)

    def __getitem__(self, key):
        value = dict.get(self, key)
        if value is None:
            value = self.load(key)
        return value

    def commit(self):
        for k, v in self.items():
            self.store(k, v)
        for k in self.deleted:
            self.delete(key)
        self.clear()
        self.deleted = []

    def rollback(self):
        self.clear()
        self.deleted = []


class ydict(xdict):
    """ Hilfsklasse zum Test von xdict:
        load laedt aus data
        store speichert nach data """

    def __init__(self, data):
        def load(k):
            return data[k]

        def store(k, v):
            data[k] = v

        def delete(k):
            del data[k]

        xdict.__init__(self, load, store, delete)


if __name__ == '__main__':
    pass
