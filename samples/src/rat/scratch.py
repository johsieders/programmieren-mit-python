## test
## js 11.08. 2004


class T(tuple):
    def __init__(self, cs):
        if len(cs) == 0:
            raise ValueError, ' no coefficients'
        self.__zero = cs[0] - cs[0]

    def zero(self):
        return self.__zero


class L(list):
    def __init__(self, xs):
        print
        'hi'
        super(L, self).__init__(xs)
