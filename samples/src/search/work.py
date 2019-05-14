## js 19.1.03


def f(n):
    if n == 0:
        yield 0
    else:
        for k in f(n-1):
            yield k
            

class T(object):
    def __init__(self, n):
        self.n = n

    def g(self):
        for i in range(self.n):
            yield i

    def __iter__(self):
        return self.g()
    
    class S(object):
        def __init__(self):
            self.x = self.n


def perm(xs):
    if len(xs) == 0:
        return []
    elif len(xs) == 1:
        return [xs]
    else:               ## len(xs) > 1
        result = []
        for i in range(0, len(xs)):
            tmp = perm(xs[:i] + xs[i+1:])
            for t in tmp:
                t.append(xs[i])
            result += tmp
        return result


def perm1(xs):
    if len(xs) < 2:
        yield [xs]
    else:               ## len(xs) > 1
        for i in range(0, len(xs)):
            for p in perm(xs[:i] + xs[i+1:]):
                p.append(xs[i])
                yield p

